import os
from dotenv import load_dotenv
import cohere
from backoffice.models import Evento
from chatbot.cache import delete_chat_history
from chatbot.chroma_client import consultar_chroma

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key=COHERE_API_KEY)

def generar_respuesta_con_rag(mensaje_usuario, historial, chat_id="test"):
    respuesta_encuesta = manejar_encuesta_si_corresponde(mensaje_usuario, historial)
    if respuesta_encuesta:
        return respuesta_encuesta

    messages = [{
    "role": "system",
    "content": (
        "Eres un asistente institucional conversacional que informa a ciudadanos sobre "
        "eventos, cursos, talleres, charlas, capacitaciones y convocatorias organizadas por una institución pública. "
        "Tu estilo es claro, respetuoso, útil y amable. "
        "Si la persona pregunta de forma general (por ejemplo, '¿Qué cursos hay?'), deberás listar los disponibles. "
        "Si la persona pregunta por una temática específica (por ejemplo, '¿Hay algo de Excel?'), buscá documentos relevantes y respondé con la información más útil. "
        "Si no encontrás información directa, intentá sugerir algo relacionado o derivar cordialmente. "
        "Siempre hablás en español neutro, con tono institucional y accesible."
        )
    }]

    for linea in historial:
        if linea.startswith("Usuario:"):
            messages.append({"role": "user", "content": linea.replace("Usuario:", "").strip()})
        elif linea.startswith("Bot:"):
            messages.append({"role": "assistant", "content": linea.replace("Bot:", "").strip()})

    messages.append({"role": "user", "content": mensaje_usuario})

    mensaje_lower = mensaje_usuario.lower()
    
    consulta_forzada = None
    palabra_detectada = None

    CATEGORIAS = {
        "curso": "lista de cursos",
        "taller": "lista de talleres",
        "charla": "lista de charlas",
        "capacitación": "lista de capacitaciones",
        "convocatoria": "lista de convocatorias",
        "evento": "lista de eventos"
    }

    for palabra, consulta in CATEGORIAS.items():
        if palabra in mensaje_lower and any(p in mensaje_lower for p in ["hay", "todos", "cuáles", "qué"]):
            consulta_forzada = consulta
            palabra_detectada = palabra
            break
    
    if consulta_forzada and palabra_detectada:
        eventos_relacionados = Evento.objects.filter(
            categoria__nombre__icontains=palabra_detectada
        ).order_by("fecha")

        if eventos_relacionados.exists():
            respuesta = f"📋 {consulta_forzada.capitalize()} disponibles:\n\n"
            for ev in eventos_relacionados:
                respuesta += f"• {ev.titulo} ({ev.fecha.strftime('%d/%m')})"
                if ev.area:
                    respuesta += f" – Área: {ev.area.nombre}"
                respuesta += "\n"

            respuesta += "\n📝 ¿Te gustaría responder una breve encuesta para mejorar el servicio? [Sí / No]"

            if "¡gracias por tu tiempo!" in respuesta.lower():
                delete_chat_history(chat_id)

            return respuesta.strip()

    print("🔎 Mensajes enviados a Cohere:")
    for m in messages:
        print(f" - {m['role']}: {m['content']}")

    print("📡 Consultando Chroma...")
    
    consulta_final = consulta_forzada or mensaje_usuario
    documentos = consultar_chroma(consulta_final, k=5)

    docs = [{"data": {"text": texto}, "metadata": metadata} for texto, metadata in documentos if texto]
    print(f"📂 Documentos encontrados: {len(documentos)}")
    
    response = co.chat(
        model="command-a-03-2025",
        messages=messages,
        documents=docs
    )
    print("📥 Respuesta recibida de Cohere:", response)
    cohere_content = response.message.content
    respuesta_texto = (
        cohere_content[0].text.strip()
        if cohere_content else "Lo siento, hubo un error al generar la respuesta."
    )
    print("✅ Respuesta generada:", respuesta_texto)
    
    if not any("¿te gustaría responder una breve encuesta" in m.get("content", "").lower() for m in messages):
        respuesta_texto += "\n\n📝 ¿Te gustaría responder una breve encuesta para mejorar el servicio? [Sí / No]"

    if "¡gracias por tu tiempo!" in respuesta_texto.lower():
        delete_chat_history(chat_id)

    return respuesta_texto

def manejar_encuesta_si_corresponde(mensaje_usuario, historial):
    msg_lower = mensaje_usuario.lower().strip()

    ofrecio_encuesta = any(
        m.startswith("Bot:") and "¿te gustaría responder una breve encuesta" in m.lower()
        for m in historial
    )
    acepto_encuesta = ofrecio_encuesta and msg_lower in ["sí", "si", "ok", "dale", "claro", "por supuesto", "sí, claro", "vale"]

    if acepto_encuesta:
        return "🙏 Gracias por aceptar. ¿Qué puntuación le darías al servicio de 1 a 5 estrellas?"

    if any("¿qué puntuación le darías" in m.lower() for m in historial):
        if msg_lower in ["1", "2", "3", "4", "5"]:
            return "🗒️ ¿Querés dejar un comentario adicional sobre cómo podemos mejorar?"

    if any("¿querés dejar un comentario adicional" in m.lower() for m in historial):
        return "🎉 ¡Gracias por tu tiempo! Tu opinión nos ayuda a mejorar."

    return None
