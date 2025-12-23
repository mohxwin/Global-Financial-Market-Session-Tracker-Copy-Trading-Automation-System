from django.db import models
from django.conf import settings

# Create your models here.

class ReferralCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='referral_codes',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} by {self.referrer.username}"


class Referral(models.Model):
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='referrals',
        on_delete=models.CASCADE
    )
    referred_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='referred_by',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.referrer.username} referred {self.referred_user.username}"
