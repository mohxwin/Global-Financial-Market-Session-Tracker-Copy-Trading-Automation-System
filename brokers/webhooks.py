from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.utils import verify_webhook

class ExnessWebhookView(APIView):
    """
    Handles Exness webhook callbacks
    """

    authentication_classes = []  # Webhooks don't use JWT
    permission_classes = []      # Verified via signature instead

    def post(self, request):
        # 1️⃣ Verify signature
        if not verify_webhook(request):
            return Response(
                {"error": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ Extract payload
        data = request.data

        # 3️⃣ TODO: dispatch event (later)
        # Example:
        # handle_exness_trade_event(data)

        return Response(
            {
                "message": "Webhook received successfully",
                "data": data
            },
            status=status.HTTP_200_OK
        )
