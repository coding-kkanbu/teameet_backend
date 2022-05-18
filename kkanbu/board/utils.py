from urllib.parse import urlencode

from rest_framework.exceptions import APIException


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def url_with_query(path, **kwargs):
    return path + "?" + urlencode(kwargs)


class UniqueBlameError(APIException):
    status_code = 400
    default_detail = "신고는 한번 밖에 할 수 없습니다."
    default_code = "unique_blame_constraint"
