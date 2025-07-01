from django.urls import path
from . import views

app_name = "backoffice"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("reindexar-chroma/", views.reindexar_chroma, name="reindexar_chroma"),
    # Eventos
    path("eventos/", views.listar_eventos, name="listar_eventos"),
    path("eventos/crear/", views.crear_evento, name="crear_evento"),
    path("eventos/<int:evento_id>/editar/", views.editar_evento, name="editar_evento"),
    path("eventos/<int:evento_id>/eliminar/", views.eliminar_evento, name="eliminar_evento"),
    # Áreas
    path("areas/", views.listar_areas, name="listar_areas"),
    path("areas/crear/", views.crear_area, name="crear_area"),
    path("areas/<int:area_id>/editar/", views.editar_area, name="editar_area"),
    path("areas/<int:area_id>/eliminar/", views.eliminar_area, name="eliminar_area"),
    # Categorías
    path("categorias/", views.listar_categorias, name="listar_categorias"),
    path("categorias/crear/", views.crear_categoria, name="crear_categoria"),
    path("categorias/<int:categoria_id>/editar/", views.editar_categoria, name="editar_categoria"),
    path("categorias/<int:categoria_id>/eliminar/", views.eliminar_categoria, name="eliminar_categoria"),
    # FAQs
    path("faqs/", views.listar_faqs, name="listar_faqs"),
    path("faqs/crear/", views.crear_faq, name="crear_faq"),
    path("faqs/<int:faq_id>/editar/", views.editar_faq, name="editar_faq"),
    path("faqs/<int:faq_id>/eliminar/", views.eliminar_faq, name="eliminar_faq"),
    # Canales
    path("canales/", views.listar_canales, name="listar_canales"),
    path("canales/nuevo/", views.crear_canal, name="crear_canal"),
    path("canales/<int:canal_id>/editar/", views.editar_canal, name="editar_canal"),
    path("canales/<int:canal_id>/eliminar/", views.eliminar_canal, name="eliminar_canal"),
    # Logs
    path("logs/", views.listar_logs, name="listar_logs"),
    path("auditorias/", views.listar_auditoria, name="listar_auditoria"),

    ]

