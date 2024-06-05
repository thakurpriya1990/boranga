from django.forms import ValidationError
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import urllib.parse

from boranga.components.spatial.models import Proxy
from boranga.components.spatial.utils import process_proxy, proxy_object


@csrf_exempt
def mapProxyView(request, request_path, path):
    if not request.user.is_authenticated:
        raise ValidationError("User is not authenticated")

    queryString = request.META["QUERY_STRING"]
    username = request.user.username
    auth_user = None
    auth_password = None

    try:
        proxy = proxy_object(request_path)
    except Proxy.DoesNotExist:
        raise Http404(f"No active Proxy entry found for {username} and {request_path}")
    else:
        if proxy.get("basic_auth_enabled"):
            auth_user = proxy.get("username")
            auth_password = proxy.get("password")
        remoteurl = proxy.get("proxy_url") + path

    params = urllib.parse.parse_qs(queryString)
    params = {k.lower(): v for k, v in params.items()}
    if "GetMap" in params.get("request", []):
        response = process_proxy(
            request, remoteurl, queryString, auth_user, auth_password
        )
    elif "GetFeature" in params.get("request", []):
        res = requests.post(remoteurl, params=params, auth=(auth_user, auth_password))
        response = HttpResponse(
            res.content,
            status=res.status_code,
            content_type=res.headers["Content-Type"],
        )
    else:
        raise Http404(f"Request {params.get('request')} not supported")

    return response
