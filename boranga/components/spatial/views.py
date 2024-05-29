from django.forms import ValidationError
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from boranga.components.spatial.models import Proxy
from boranga.components.spatial.utils import process_proxy
from boranga.helpers import is_internal


def proxy_object(request_path):
    try:
        proxy = Proxy.objects.get(
            active=True,
            request_path=request_path,
        )
    except Proxy.DoesNotExist:
        raise
    else:
        return proxy

@csrf_exempt
def mapProxyView(request, request_path, path):
    if not request.user.is_authenticated:
        raise ValidationError("User is not authenticated")

    if not is_internal(request):
        raise ValidationError("User is not an internal user")

    queryString = request.META["QUERY_STRING"]
    username = request.user.username
    auth_user = None
    auth_password = None

    try:
        proxy = proxy_object(request_path)
    except Proxy.DoesNotExist:
        raise Http404(f"No active Proxy entry found for {username} and {request_path}")
    else:
        if proxy.basic_auth_enabled:
            auth_user = proxy.username
            auth_password = proxy.password
        remoteurl = proxy.proxy_url + path

    response = process_proxy(request, remoteurl, queryString, auth_user, auth_password)
    return response
