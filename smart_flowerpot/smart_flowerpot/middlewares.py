import socket
from django.conf import settings

class DynamicAllowedHostsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host_ip = request.get_host().split(':')[0]
        if host_ip not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append(host_ip)
        return self.get_response(request)