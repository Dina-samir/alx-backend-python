from datetime import datetime
from django.http import HttpResponseForbidden
import logging
from datetime import datetime

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Allowed only between 6 PM (18:00) and 9 PM (21:00)
        if not (now.hour >= 18 and now.hour < 21):
            return HttpResponseForbidden("Access to the chat is restricted at this time.")
        return self.get_response(request)




class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up the logger
        self.logger = logging.getLogger('request_logger')
        handler = logging.FileHandler('request.logs')  
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
