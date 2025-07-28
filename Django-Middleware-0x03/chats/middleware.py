from datetime import datetime
from django.http import HttpResponseForbidden
import logging
from datetime import datetime
from django.http import JsonResponse
import time 

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Allowed only between 6 PM (18:00) and 9 PM (21:00)
        if not (now.hour >= 18 and now.hour < 21):
            return HttpResponseForbidden("Access to the chat is restricted at this time.")
        return self.get_response(request)



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = {}

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/api/messages"):
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 60 seconds
            limit = 5

            # Keep only timestamps within the last minute
            timestamps = [t for t in self.request_log.get(ip, []) if now - t < window]

            if len(timestamps) >= limit:
                return JsonResponse(
                    {"detail": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429,
                )

            timestamps.append(now)
            self.request_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
    

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up the logger
        self.logger = logging.getLogger('request_logger')
        handler = logging.FileHandler('requests.log')  
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check for authenticated requests
        if request.user.is_authenticated:
            # Only restrict certain paths, e.g., paths that start with /api/admin-actions/
            if request.path.startswith('/api/admin-actions/'):
                user_role = getattr(request.user, 'role', None) 

                if user_role not in ['admin', 'moderator']:
                    return JsonResponse(
                        {'detail': 'Permission denied. Admin or Moderator role required.'},
                        status=403
                    )

        return self.get_response(request)