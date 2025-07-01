from django import forms
from .models import Evento, Area, Categoria, FAQ, Canal

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'cuerpo', 'fecha', 'categoria', 'area']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
        }

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['pregunta', 'respuesta']
        widgets = {
            'pregunta': forms.TextInput(attrs={'class': 'form-control'}),
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
class CanalForm(forms.ModelForm):
    class Meta:
        model = Canal
        fields = ["nombre", "plataforma", "page_id", "page_access_token", "verify_token", "activo"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'plataforma': forms.Select(attrs={'class': 'form-select'}),
            'page_id': forms.TextInput(attrs={'class': 'form-control'}),
            "page_access_token": forms.TextInput(attrs={"type": "password", "id": "page_access_token_field"}),
            'verify_token': forms.TextInput(attrs={'class': 'form-control'}),
        }