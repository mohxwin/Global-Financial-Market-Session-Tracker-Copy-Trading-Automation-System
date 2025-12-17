from django.urls import path
from .webhooks import ExnessWebhookView

urlpatterns = [
    path("exness/webhook/", ExnessWebhookView.as_view(), name="exness-webhook"),
]
