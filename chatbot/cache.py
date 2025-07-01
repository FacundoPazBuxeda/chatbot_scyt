from django.core.cache import cache
from datetime import datetime

def get_chat_history(chat_id):
    return cache.get(f"chat:{chat_id}", [])

def update_chat_history(chat_id, message):
    history = cache.get(f"chat:{chat_id}", [])
    history.append(message)
    cache.set(f"chat:{chat_id}", history, timeout=300)  # 5 minutos TTL

def delete_chat_history(chat_id):
    cache.delete(f"chat:{chat_id}")
    
def update_last_interaction_time(chat_id):
    cache.set(f"last_seen_{chat_id}", datetime.now(), timeout=60 * 60 * 24)

def get_last_interaction_time(chat_id):
    return cache.get(f"last_seen_{chat_id}")