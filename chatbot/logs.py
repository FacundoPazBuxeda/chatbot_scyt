from backoffice.models import LogInteraccion

def guardar_log(chat_id, mensaje_usuario, respuesta_bot, message_id=None):
    if message_id and LogInteraccion.objects.filter(message_id=message_id).exists():
        print(f"⚠️ Ya se procesó el message_id {message_id}, evitando duplicado")
        return

    LogInteraccion.objects.create(
        chat_id=chat_id,
        mensaje_usuario=mensaje_usuario,
        respuesta_bot=respuesta_bot,
        message_id=message_id
    )
