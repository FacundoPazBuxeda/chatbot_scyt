def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")


def registrar_auditoria(request, accion, modelo, objeto_id, descripcion=""):
    from .models import Auditoria  # Evita import circular si estás en views
    Auditoria.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        accion=accion,
        modelo=modelo,
        objeto_id=objeto_id,
        descripcion=descripcion,
        ip=get_client_ip(request)
    )
