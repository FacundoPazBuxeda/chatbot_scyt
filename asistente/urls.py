from django.contrib import admin
from django.urls import path, include
from backoffice.views import webhook_mensajes

urlpatterns = [
    path("admin/", admin.site.urls),
    path("backoffice/", include("backoffice.urls")),
    path("webhook/meta/", webhook_mensajes, name="webhook_mensajes"),
]
