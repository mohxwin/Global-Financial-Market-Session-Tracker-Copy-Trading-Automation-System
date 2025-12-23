from django.urls import path
from .views import CoinWalletView



urlpatterns = [
    path('', CoinWalletView.as_view(), name='coin_wallet'),
]
