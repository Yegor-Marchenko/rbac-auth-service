from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings


def create_jwt(user):
    """Создаёт JWT с id пользователя, версией токена и сроком на сутки."""
    payload = {
        'user_id': user.id,
        'token_version': user.token_version,
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
