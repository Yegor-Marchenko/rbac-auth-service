from rest_framework.authentication import BaseAuthentication


class MiddlewareAuthentication(BaseAuthentication):
    """
    Передаёт DRF пользователя, уже опознанного JWTAuthenticationMiddleware
    на уровне Django запроса. Обращение к request._request используется для
    доступ к нижележащему HttpRequest (по аналогии с SessionAuthentication
    в DRF).
    """

    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if user is None or not user.is_authenticated:
            return None
        return (user, None)
