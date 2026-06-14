from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidCredentials(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Неверный email или пароль'


class NotAuthenticatedError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Учётные данные не были предоставлены'
