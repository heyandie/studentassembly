from django.conf import settings
from django.http import HttpResponseRedirect


class SSLMiddleware(object):

    def process_request(self, request):
        if request.META.get("HTTP_X_FORWARDED_PROTO", "") == 'http':
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace("http://", "https://")
            return HttpResponseRedirect(secure_url)
