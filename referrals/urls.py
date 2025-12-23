from django.urls import path
from .views import ReferralView, ReferralCodeView


urlpatterns = [
    path('referral-codes/', ReferralCodeView.as_view(), name='referral-codes'),
    path('referrals/', ReferralView.as_view(), name='referrals'),
]
