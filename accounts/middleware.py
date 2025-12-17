from user_agents import parse
from .models import LoginHistory

class LoginTrackingMiddleware:
    """
    Middleware to track user's IP and device on each request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            ua = parse(request.META.get("HTTP_USER_AGENT", ""))
            ip = request.META.get("REMOTE_ADDR")
            
            # Save login history
            LoginHistory.objects.create(
                user=request.user,
                ip_address=ip,
                device=f"{ua.browser.family} {ua.browser.version_string} | {ua.os.family} {ua.os.version_string} | {ua.device.family}"
            )
        return response
