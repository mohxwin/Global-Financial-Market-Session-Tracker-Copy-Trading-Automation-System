from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings
from uuid import uuid4


from .models import ReferralCode


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a referral code for newly created users.
    """
    if created:
        with transaction.atomic():
            # Generate unique code
            code = get_random_string(10)
            
            # Check for uniqueness (very low probability but good practice)
            while ReferralCode.objects.filter(code=code).exists():
                code = get_random_string(10)
            
            ReferralCode.objects.create(referrer=instance, code=code)    
      