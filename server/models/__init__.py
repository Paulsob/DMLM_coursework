# server/models/__init__.py
# Импортируем ключевые модели, чтобы к ним можно было обращаться напрямую

from .music_model import Music
from . import images, text, music

__all__ = ["Music", "images", "text", "music"]
