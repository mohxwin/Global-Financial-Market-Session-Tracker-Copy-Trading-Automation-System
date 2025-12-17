from cryptography.fernet import Fernet
import hmac
import hashlib
from django.conf import settings
from user_agents import parse

# Generate a key once and store it securely (do NOT regenerate on each run)
FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)


"""Encrypt API key"""
def encrypt_api_key(api_key: str) -> bytes:
    return cipher.encrypt(api_key.encode())

"""Decrypt API key"""
def decrypt_api_key(encrypted_key: bytes) -> str:
    return cipher.decrypt(encrypted_key).decode()


"""
    Verify API signature.
    payload: raw request body
    signature: header signature from broker
    secret: your broker API secret
    """
def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    computed = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, signature)


"""
    Verify webhook request signature.
    Assumes the broker sends signature in 'X-SIGNATURE' header.
    """
def verify_webhook(request) -> bool:
    signature = request.headers.get("X-SIGNATURE", "")
    secret = settings.WEBHOOK_SECRET  # Add to your settings.py
    return verify_signature(request.body, signature, secret)



def parse_user_agent(request):
    ua_string = request.META.get("HTTP_USER_AGENT", "")
    ua = parse(ua_string)
    ip = request.META.get("REMOTE_ADDR")
    device = f"{ua.browser.family} {ua.browser.version_string} | {ua.os.family} {ua.os.version_string} | {ua.device.family}"
    return ip, device
