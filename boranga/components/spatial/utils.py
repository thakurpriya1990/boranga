from django.apps import apps
from django.views.decorators.csrf import csrf_exempt

from boranga import settings


def get_proxy_cache(app_label, model_name):
    from django.core.cache import cache

    cache_key = settings.CACHE_KEY_PROXY_LAYER_DATA.format(
        app_label=app_label, model_name=model_name
    )
    proxy_cache_dumped_data = cache.get(cache_key)
    proxy_cache_array = []

    if proxy_cache_dumped_data is None:
        proxy_cache_query = apps.get_model(app_label, model_name).objects.all()

        for pr in proxy_cache_query:
            proxy_cache_array.append({"layer_name": pr.layer_name, "cache_expiry": 300})

        cache.set(cache_key, proxy_cache_array, 86400)
    else:
        proxy_cache_array = proxy_cache_dumped_data

    return proxy_cache_array


@csrf_exempt
def process_proxy(request, remoteurl, queryString, auth_user, auth_password):
    from django.http import HttpResponse
    from django.core.cache import cache
    from wagov_utils.components.proxy.views import proxy_view
    import base64
    import json

    if request.user.is_authenticated:
        proxy_cache = None
        proxy_response = None
        proxy_response_content = None
        base64_json = {}
        query_string_remote_url = remoteurl + "?" + queryString

        cache_times_strings = get_proxy_cache("boranga", "tilelayer")
        CACHE_EXPIRY = 300
        layer_allowed = False

        proxy_cache = cache.get(query_string_remote_url)
        query_string_remote_url_new = query_string_remote_url.replace("%3A", ":")
        for cts in cache_times_strings:
            layer_name = cts["layer_name"].split(":")[-1]
            if layer_name in query_string_remote_url:
                CACHE_EXPIRY = cts["cache_expiry"]

            if (
                "?layer=" + cts["layer_name"] in query_string_remote_url_new
                or "&LAYERS=" + cts["layer_name"] in query_string_remote_url_new
            ):
                layer_allowed = True
        if layer_allowed is True:
            if proxy_cache is None:
                auth_details = None
                if auth_user is None and auth_password is None:
                    auth_details = None
                else:
                    auth_details = {"user": auth_user, "password": auth_password}
                proxy_response = proxy_view(request, remoteurl, basic_auth=auth_details)
                proxy_response_content_encoded = base64.b64encode(
                    proxy_response.content
                )
                base64_json = {
                    "status_code": proxy_response.status_code,
                    "content_type": proxy_response.headers["content-type"],
                    "content": proxy_response_content_encoded.decode("utf-8"),
                    "cache_expiry": CACHE_EXPIRY,
                }
                if proxy_response.status_code == 200:
                    cache.set(
                        query_string_remote_url, json.dumps(base64_json), CACHE_EXPIRY
                    )
                else:
                    cache.set(query_string_remote_url, json.dumps(base64_json), 15)
            else:
                base64_json = json.loads(proxy_cache)
            proxy_response_content = base64.b64decode(base64_json["content"].encode())
            http_response = HttpResponse(
                proxy_response_content,
                content_type=base64_json["content_type"],
                status=base64_json["status_code"],
            )
            http_response["Django-Cache-Expiry"] = (
                str(base64_json["cache_expiry"]) + " seconds"
            )
            return http_response
        else:
            http_response = HttpResponse(
                "Access Denied", content_type="text/html", status=401
            )
            return http_response
    return
