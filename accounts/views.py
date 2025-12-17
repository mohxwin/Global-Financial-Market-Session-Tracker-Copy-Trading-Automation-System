import base64
import io
import logging
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings

import qrcode
import pyotp

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit

from .models import LoginHistory
from .serializers import RegisterSerializer, TwoFAVerifySerializer
from core.utils import parse_user_agent

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

User = get_user_model()
logger = logging.getLogger(__name__)


# -----------------------------
# User Registration
# -----------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"message": "Account created successfully"},
                status=status.HTTP_201_CREATED
            )

        except IntegrityError:
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.exception("Registration failed")
            return Response(
                {"error": "Registration failed", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# -----------------------------
# JWT Login with 2FA enforcement
# -----------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key="ip", rate="5/m", block=True))
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                return Response(
                    {"error": "Email and password required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(request, email=email, password=password)
            if not user:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # -------------------------
            # 2FA enforcement
            # -------------------------
            if user.is_2fa_enabled:
                if user.two_fa_method == "authenticator":
                    return Response(
                        {"2fa_required": True, "user_id": user.id, "method": "authenticator"},
                        status=status.HTTP_200_OK
                    )
                elif user.two_fa_method == "email":
                    # Generate temporary OTP and send via email
                    otp = pyotp.random_base32()[:6]  # 6-char OTP
                    user.email_otp = otp
                    user.save()
                    send_mail(
                        subject="Your TradingApp OTP",
                        message=f"Your OTP is: {otp}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    return Response(
                        {"2fa_required": True, "user_id": user.id, "method": "email"},
                        status=status.HTTP_200_OK
                    )

            # -------------------------
            # Issue JWT (no 2FA)
            # -------------------------
            refresh = RefreshToken.for_user(user)

            # Track IP & device
            ip, device = parse_user_agent(request)
            LoginHistory.objects.create(user=user, ip_address=ip, device=device)

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
                status=status.HTTP_200_OK, 
                data={user}
            )

        except Exception as e:
            logger.exception("Login failed")
            return Response(
                {"error": "Login failed", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# -----------------------------
# 2FA Verification (TOTP or Email)
# -----------------------------
class TwoFAVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = TwoFAVerifySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user_id = serializer.validated_data["user_id"]
            otp = serializer.validated_data["otp"]

            user = User.objects.get(id=user_id)

            if user.two_fa_method == "authenticator":
                totp = pyotp.TOTP(user.otp_secret)
                if not totp.verify(otp, valid_window=1):
                    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            elif user.two_fa_method == "email":
                if otp != user.email_otp:
                    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
                user.email_otp = None
                user.save()

            # Issue JWT after successful 2FA
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("2FA verification failed")
            return Response(
                {"error": "2FA verification failed", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# -----------------------------
# Enable 2FA
# -----------------------------
class Enable2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            method = request.data.get("method", "authenticator")
            user = request.user

            user.is_2fa_enabled = True
            user.two_fa_method = method

            if method == "authenticator":
                secret = pyotp.random_base32()
                user.otp_secret = secret
                user.save()

                # Provisioning URI for authenticator apps
                otp_uri = pyotp.TOTP(secret).provisioning_uri(
                    name=user.email,
                    issuer_name="TradingApp"
                )

                # Generate QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(otp_uri)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                qr_base64 = base64.b64encode(buffered.getvalue()).decode()

                return Response({
                    "message": "Authenticator 2FA enabled",
                    "secret": secret,
                    "otp_uri": otp_uri,
                    "qr_code_base64": qr_base64
                }, status=status.HTTP_200_OK)

            elif method == "email":
                user.save()
                return Response({"message": "Email 2FA enabled"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Enable 2FA failed")
            return Response(
                {"error": "Unable to enable 2FA", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class GoogleLoginJWTView(SocialLoginView):
    """
    Google OAuth login with JWT + 2FA enforcement.
    """
    adapter_class = GoogleOAuth2Adapter
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Exchange Google OAuth token for JWT
        """
        try:
            # Call the parent SocialLoginView
            response = super().post(request, *args, **kwargs)
            user = self.user

            # Enforce 2FA if enabled
            if user.is_2fa_enabled:
                if user.two_fa_method == "authenticator":
                    return Response({
                        "2fa_required": True,
                        "user_id": user.id,
                        "method": "authenticator"
                    }, status=status.HTTP_200_OK)

                elif user.two_fa_method == "email":
                    # Generate email OTP
                    import pyotp
                    from django.core.mail import send_mail
                    otp = pyotp.random_base32()[:6]
                    user.email_otp = otp
                    user.save()
                    send_mail(
                        subject="Your TradingApp OTP",
                        message=f"Your OTP is: {otp}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    return Response({
                        "2fa_required": True,
                        "user_id": user.id,
                        "method": "email"
                    }, status=status.HTTP_200_OK)

            # Track IP & device
            ip, device = parse_user_agent(request)
            LoginHistory.objects.create(user=user, ip_address=ip, device=device)

            # Return JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("Google login failed")
            return Response({"error": "Google login failed", "detail": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)