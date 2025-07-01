import uuid
from datetime import timedelta
from django.utils import timezone
from backoffice.models import ChatSession
from django.db import IntegrityError

def obtener_o_crear_session(user_id, max_duracion_minutos=30):
    ahora = timezone.now()
    expiracion = ahora - timedelta(minutes=max_duracion_minutos)

    sesion = ChatSession.objects.filter(user_id=user_id, created_at__gte=expiracion).first()
    if sesion:
        return sesion.session_id

    for _ in range(3):  # Intentar hasta 3 veces en caso de colisión
        try:
            session_id = str(uuid.uuid4())
            ChatSession.objects.create(user_id=user_id, session_id=session_id)
            return session_id
        except IntegrityError:
            continue
    raise Exception("❌ No se pudo crear una sesión de chat única")
