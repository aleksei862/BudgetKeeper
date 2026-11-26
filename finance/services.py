import hashlib
import secrets
from datetime import timedelta
from django.utils import timezone
from .models import PasswordResetToken

TOKEN_TTL_MINUTES = 30


def create_reset_token(user):
    # 1. Генерируем случайный токен
    raw_token = secrets.token_urlsafe(32)

    # 2. Хешируем его (в базе храним только хеш)
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

    # 3. Сохраняем в базу
    PasswordResetToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=timezone.now() + timedelta(minutes=TOKEN_TTL_MINUTES),
    )

    # 4. Возвращаем "сырой" токен (его мы отправим на почту пользователю)
    return raw_token


def get_token_by_raw(raw_token):
    # Ищем токен в базе по его хешу
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    return PasswordResetToken.objects.filter(token_hash=token_hash).first()