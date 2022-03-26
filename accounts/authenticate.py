from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

from rest_framework.authentication import CSRFCheck
from django.middleware.csrf import CsrfViewMiddleware

from rest_framework import exceptions


def enforce_crsf(request):
    check = CSRFCheck(CsrfViewMiddleware)
    check.process_request(request)

    reason = check.process_view(
        request,
        None,
        (), {}
    )
    if reason:
        raise exceptions.PermissionDenied(f"CSRF failed: {reason}")


class AppAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(
                settings.SIMPLE_JWT["AUTH_COOKIE"]) or None

        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        # enforce_crsf(request)
        return self.get_user(validated_token), validated_token
