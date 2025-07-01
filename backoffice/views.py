import json
import requests
import os
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from chatbot.chroma_client import reindexar_base_conocimiento
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import datetime, timedelta

from chatbot.session_utils import obtener_o_crear_session
from .utils import registrar_auditoria

from .models import Evento, Area, Categoria, FAQ, LogInteraccion, Canal, Auditoria
from .forms import EventoForm, AreaForm, CategoriaForm, FAQForm, CanalForm

from chatbot.chroma_client import consultar_chroma
from chatbot.cohere_client import generar_respuesta_con_rag
from chatbot.cache import (
    get_chat_history, update_chat_history, delete_chat_history,
    get_last_interaction_time, update_last_interaction_time
)
from chatbot.logs import guardar_log


FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
MAX_IDLE_MINUTES = 15

@staff_member_required
def reindexar_chroma(request):
    reindexar_base_conocimiento()
    messages.success(request, "La base de conocimiento fue reindexada correctamente.")
    return redirect("backoffice:dashboard")

@staff_member_required
def dashboard(request):
    return render(request, "backoffice/dashboard.html")

# |------------------------------------------------------------------------------|

# EVENTOS
@staff_member_required
def listar_eventos(request):
    eventos = Evento.objects.select_related("categoria", "area").order_by("-fecha")
    return render(request, "backoffice/eventos/listar.html", {"eventos": eventos})

@staff_member_required
def crear_evento(request):
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("backoffice:listar_eventos")
    else:
        form = EventoForm()
    return render(request, "backoffice/eventos/formulario.html", {"form": form, "modo": "crear"})

@staff_member_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            registrar_auditoria(request, "Editó", "Evento", str(evento.id), f"Título: {evento.titulo}")
            return redirect("backoffice:listar_eventos")
    else:
        form = EventoForm(instance=evento)
    return render(request, "backoffice/eventos/formulario.html", {"form": form, "modo": "editar"})

@staff_member_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    evento.delete()
    return redirect("backoffice:listar_eventos")

# ÁREAS
@staff_member_required
def listar_areas(request):
    areas = Area.objects.all()
    return render(request, "backoffice/areas/listar.html", {"areas": areas})

@staff_member_required
def crear_area(request):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("backoffice:listar_areas")
    return render(request, "backoffice/areas/formulario.html", {"form": form, "modo": "crear"})

@staff_member_required
def editar_area(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    form = AreaForm(request.POST or None, instance=area)
    if form.is_valid():
        form.save()
        return redirect("backoffice:listar_areas")
    return render(request, "backoffice/areas/formulario.html", {"form": form, "modo": "editar"})

@staff_member_required
def eliminar_area(request, area_id):
    get_object_or_404(Area, pk=area_id).delete()
    return redirect("backoffice:listar_areas")

# CATEGORÍAS
@staff_member_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "backoffice/categorias/listar.html", {"categorias": categorias})

@staff_member_required
def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("backoffice:listar_categorias")
    return render(request, "backoffice/categorias/formulario.html", {"form": form, "modo": "crear"})

@staff_member_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect("backoffice:listar_categorias")
    return render(request, "backoffice/categorias/formulario.html", {"form": form, "modo": "editar"})

@staff_member_required
def eliminar_categoria(request, categoria_id):
    get_object_or_404(Categoria, pk=categoria_id).delete()
    return redirect("backoffice:listar_categorias")

# FAQS
@staff_member_required
def listar_faqs(request):
    faqs = FAQ.objects.all()
    return render(request, "backoffice/faqs/listar.html", {"faqs": faqs})

@staff_member_required
def crear_faq(request):
    form = FAQForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("backoffice:listar_faqs")
    return render(request, "backoffice/faqs/formulario.html", {"form": form, "modo": "crear"})

@staff_member_required
def editar_faq(request, faq_id):
    faq = get_object_or_404(FAQ, pk=faq_id)
    form = FAQForm(request.POST or None, instance=faq)
    if form.is_valid():
        form.save()
        return redirect("backoffice:listar_faqs")
    return render(request, "backoffice/faqs/formulario.html", {"form": form, "modo": "editar"})

@staff_member_required
def eliminar_faq(request, faq_id):
    get_object_or_404(FAQ, pk=faq_id).delete()
    return redirect("backoffice:listar_faqs")

# CANALES
@staff_member_required
def listar_canales(request):
    canales = Canal.objects.all().order_by("nombre")
    return render(request, "backoffice/canales/listar.html", {"canales": canales})

@staff_member_required
def crear_canal(request):
    if request.method == "POST":
        form = CanalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("backoffice:listar_canales")
    else:
        form = CanalForm()
    return render(request, "backoffice/canales/formulario.html", {"form": form, "modo": "crear"})

@staff_member_required
def editar_canal(request, canal_id):
    canal = get_object_or_404(Canal, pk=canal_id)
    if request.method == "POST":
        form = CanalForm(request.POST, instance=canal)
        if form.is_valid():
            form.save()
            return redirect("backoffice:listar_canales")
    else:
        form = CanalForm(instance=canal)
    return render(request, "backoffice/canales/formulario.html", {"form": form, "modo": "editar"})

@staff_member_required
def eliminar_canal(request, canal_id):
    canal = get_object_or_404(Canal, pk=canal_id)
    canal.delete()
    return redirect("backoffice:listar_canales")


# LOGS Y AUDITORIAS
@staff_member_required
def listar_logs(request):
    logs = LogInteraccion.objects.order_by("-timestamp")
    paginator = Paginator(logs, 30)  # 30 logs por página
    page = request.GET.get("page")
    logs_paginados = paginator.get_page(page)
    return render(request, "backoffice/logs/listar.html", {"logs": logs_paginados})

@staff_member_required
def listar_auditoria(request):
    logs = Auditoria.objects.select_related("usuario").order_by("-timestamp")[:200]
    paginator = Paginator(logs, 30)  # 30 logs por página
    page = request.GET.get("page")
    logs_paginados = paginator.get_page(page)
    return render(request, "backoffice/auditorias/listar.html", {"logs": logs_paginados})

# FACEBOOK E INSTAGRAM
@csrf_exempt
def webhook_mensajes(request):
    if request.method == "GET":
        verify_token = request.GET.get("hub.verify_token")
        if request.GET.get("hub.mode") == "subscribe" and verify_token:
            return HttpResponse(request.GET.get("hub.challenge"))
        return HttpResponse("Error de verificación", status=403)

    elif request.method == "POST":
        payload = json.loads(request.body)

        for entry in payload.get("entry", []):
            plataforma = 'facebook'

            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message", {}).get("is_echo"):
                    print("⚠️ Mensaje de eco ignorado")
                    continue
                
                sender_id = messaging_event["sender"]["id"]

                if "message" in messaging_event and "text" in messaging_event["message"]:
                    mensaje = messaging_event["message"]["text"]
                    message_id = messaging_event["message"].get("mid")

                    session_id = obtener_o_crear_session(sender_id)

                    print(f"\n📥 [{plataforma.upper()}] Mensaje de {sender_id}: {mensaje}")
                    
                    if es_nueva_conversacion(sender_id):
                        delete_chat_history(sender_id)
                    update_last_interaction_time(sender_id)
                    
                    historial = get_chat_history(session_id)
                    respuesta = generar_respuesta_con_rag(mensaje, historial, chat_id=session_id)
                    print(f"🤖 Respuesta generada: {respuesta[:80]}...")

                    update_chat_history(session_id, f"Usuario: {mensaje}")
                    update_chat_history(session_id, f"Bot: {respuesta}")

                    guardar_log(session_id, mensaje, respuesta, message_id=message_id)

                    enviar_respuesta(sender_id, respuesta, FB_PAGE_ACCESS_TOKEN)

        return JsonResponse({"status": "ok"})

def enviar_respuesta(recipient_id, mensaje, page_access_token):
    url = 'https://graph.facebook.com/v21.0/me/messages'
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": mensaje},
        "messaging_type": "RESPONSE"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {page_access_token}"
    }

    try:
        print("📤 Enviando respuesta a Facebook:", mensaje)
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error al enviar mensaje a Facebook: {e}")
        print("🔁 Respuesta de Facebook:", response.text)

def es_nueva_conversacion(chat_id):
    ultima = get_last_interaction_time(chat_id)
    if not ultima:
        return True
    return datetime.now() - ultima > timedelta(minutes=MAX_IDLE_MINUTES)