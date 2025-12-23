from django.urls import path
from .views import TradeProfileView, ExchangeAccountView, TradeView, TradeSessionView


urlpatterns = [
    path('trade-profiles/', TradeProfileView.as_view(), name='trade-profiles'),
    path('exchange-accounts/', ExchangeAccountView.as_view(), name='exchange-accounts'),
    path('trades/', TradeView.as_view(), name='trades'),
    path('trade-sessions/', TradeSessionView.as_view(), name='trade-sessions'),
]
