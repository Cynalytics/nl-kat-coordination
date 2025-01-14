import structlog
from django.http import HttpResponseForbidden
from knox.auth import TokenAuthentication
from rest_framework.exceptions import APIException


def AuthTokenMiddleware(get_response):
    def middleware(request):
        if not request.user.is_authenticated and "authorization" in request.headers:
            authenticator = TokenAuthentication()
            try:
                user_and_token = authenticator.authenticate(request)
            except APIException:
                return HttpResponseForbidden("Invalid token\n")
            else:
                if user_and_token:
                    request.user = user_and_token[0]
                    structlog.contextvars.bind_contextvars(auth_method="token")

        return get_response(request)

    return middleware
