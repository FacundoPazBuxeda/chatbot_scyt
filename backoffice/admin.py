from django.contrib import admin
from .models import Categoria, Area, Evento, FAQ, LogInteraccion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'correo']
    search_fields = ['nombre']

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha', 'categoria', 'area']
    search_fields = ['titulo', 'cuerpo']
    list_filter = ['categoria', 'area', 'fecha']
    date_hierarchy = 'fecha'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['pregunta']
    search_fields = ['pregunta', 'respuesta']

@admin.register(LogInteraccion)
class LogAdmin(admin.ModelAdmin):
    list_display = ["chat_id", "canal", "mensaje_usuario", "respuesta_bot", "timestamp"]
    list_filter = ["canal", "timestamp"]
    search_fields = ["chat_id", "mensaje_usuario", "respuesta_bot"]