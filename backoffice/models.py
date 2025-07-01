from django.db import models
from django.contrib.auth.models import User

class Canal(models.Model):
    nombre = models.CharField(max_length=100)
    plataforma = models.CharField(max_length=20, choices=[('facebook', 'Facebook'), ('instagram', 'Instagram')])
    page_id = models.CharField(max_length=100, unique=True)
    page_access_token = models.CharField(max_length=100, unique=True)
    verify_token = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.plataforma})"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Area(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    fecha = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo

class FAQ(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()

    def __str__(self):
        return self.pregunta

class LogInteraccion(models.Model):
    chat_id = models.CharField(max_length=100)
    mensaje_usuario = models.TextField()
    respuesta_bot = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    canal = models.ForeignKey(Canal, on_delete=models.SET_NULL, null=True)
    message_id = models.CharField(max_length=100, blank=True, null=True, unique=True)

class ChatSession(models.Model):
    user_id = models.CharField(max_length=100)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Auditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=255)
    modelo = models.CharField(max_length=100)
    objeto_id = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion} ({self.modelo} #{self.objeto_id})"
