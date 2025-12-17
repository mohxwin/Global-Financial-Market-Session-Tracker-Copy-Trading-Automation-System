from django.urls import path
from .views import LoginView, RegisterView, Enable2FAView, TwoFAVerifyView



urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("2fa/verify/", TwoFAVerifyView.as_view(), name="2fa-verify"),
    path("2fa/enable/", Enable2FAView.as_view(), name="two-factor-enable"),
]
