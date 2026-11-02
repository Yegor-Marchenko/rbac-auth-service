import jwt
from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class JWTAuthenticationMiddleware:
    """
    Опознаёт пользователя по JWT из заголовка Authorization: Bearer.
    При валидном токене ставит request.user; при отсутствии токена не
    вмешивается; при недействительном делает пользователя анонимным.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = self.authenticate(request)
        if user is not None:
            request.user = user
        response = self.get_response(request)
        return response

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        parts = auth_header.split()
        if len(parts) != 2:
            return None


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
