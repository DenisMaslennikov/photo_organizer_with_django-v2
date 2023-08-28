from rest_framework.exceptions import APIException


class DoesNotExist(APIException):
    status_code = 400
    default_detail = "Некорректный ID"


class NotAuthorError(APIException):
    status_code = 403
    default_detail = "Можно изменять только свои изображения"
