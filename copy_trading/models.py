from django.db import models
from django.conf import settings

# Create your models here.
class CopiedTrade(models.Model):
    trade = models.ForeignKey("trading.Trade", on_delete=models.CASCADE)
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    executed = models.BooleanField(default=False)
    execution_price = models.FloatField(null=True, blank=True)
    execution_time = models.DateTimeField(null=True, blank=True)

    error_message = models.TextField(blank=True)
