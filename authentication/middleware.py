import hashlib
from django.utils import timezone

import jwt
from django.conf import settings

from authentication.anonymous import AnonymousUser
from authentication.models import User, Session


class JWTAuthenticationMiddleware:
    """
    Опознаёт пользователя по JWT из заголовка Authorization: Bearer.
    При валидном токене ставит request.user; при отсутствующим
    или при недействительном токине делает пользователя анонимным.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = self.authenticate(request)
        response = self.get_response(request)
        return response

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return AnonymousUser()

        parts = auth_header.split()
        if len(parts) != 2:
            return AnonymousUser()

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'],
            )
        except jwt.PyJWTError:
            return AnonymousUser()

        user = User.objects.filter(id=payload.get('user_id')).first()

        if user is None or not user.is_active:
            return AnonymousUser()

        if payload.get('token_version') != user.token_version:
            return AnonymousUser()

        return user


class SessionAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.user = self.authenticate(request)
        response = self.get_response(request)
        return response

    def authenticate(self, request):
        session_id = request.COOKIES.get('session_id')
        if session_id is None:
            return AnonymousUser()

        hashed_token = hashlib.sha256(session_id.encode('utf-8')).hexdigest()
        session = Session.objects.filter(session_key_hash=hashed_token).first()

        if session is None or session.expires_at <= timezone.now():
            return AnonymousUser()

        if not session.user.is_active:
            return AnonymousUser()

        return session.user
