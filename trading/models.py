from django.db import models
from django.conf import settings

# Create your models here.

class TradeProfile(models.Model):
    """Model to store user-specific trading preferences and settings."""
    
    RISK_LEVEL = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    risk_level = models.CharField(max_length=50, default='medium', choices=RISK_LEVEL)
    base_lot_size = models.FloatField(default=0.01)
    max_daily_loss = models.FloatField()
    auto_pilot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Trade Profile"

class ExchangeAccount(models.Model):
    """Model to store user's exchange account details."""
    BINANCE = 'binance'
    EXNESS = 'exness'

    EXCHANGE_CHOICES = [
        (BINANCE, 'Binance'),
        (EXNESS, 'Exness'),
    ]

    DEMO = 'demo'
    LIVE = 'live'

    ACCOUNT_TYPE = [
        (DEMO, 'Demo'),
        (LIVE, 'Live'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICES)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    account_id = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    api_secret = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s {self.exchange} Account"

    def save(self, *args, **kwargs):
        # Ensure only one active account per user per exchange
        if self.is_active:
            ExchangeAccount.objects.filter(
                user=self.user,
                exchange=self.exchange,
                is_active=True
            ).update(is_active=False)
        super().save(*args, **kwargs)
        

class TradeSession(models.Model):
    """Model to represent different trading session."""
    OPEN = 'open'
    ACTIVE = 'active'
    CLOSED = 'closed'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    started_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)



class Trade(models.Model):
    """Model to represent individual trades executed by users."""
    BUY = 'buy'
    SELL = 'sell'

    TRADE_TYPE = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    trader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exchange = models.CharField(max_length=20, null=True, blank=True)
    symbol = models.CharField(max_length=20)
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPE)

    entry_price = models.FloatField()
    stop_loss = models.FloatField(null=True, blank=True)
    take_profit = models.FloatField(null=True, blank=True)

    is_closed = models.BooleanField(default=False)
    opened_at = models.DateTimeField(auto_now_add=True)
