from django.contrib import admin
from .models import TradeProfile, ExchangeAccount, Trade, TradeSession

# Register your models here.

class TradeProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username', )
    readonly_fields = ('created_at', 'updated_at')
    
admin.site.register(TradeProfile, TradeProfileAdmin)

class ExchangeAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'exchange', 'account_id', 'created_at', 'updated_at')
    search_fields = ('user__username', 'exchange', 'account_id')
    readonly_fields = ('created_at', 'updated_at')
    
admin.site.register(ExchangeAccount, ExchangeAccountAdmin)

class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'trader', 'trade_type', 'entry_price', 'symbol', 'opened_at')
    search_fields = ('trader__username', 'trade_type', 'symbol')
    readonly_fields = ('opened_at',)
    
admin.site.register(Trade, TradeAdmin)

class TradeSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'started_at', 'closed_at')
    search_fields = ('status',)
    readonly_fields = ('started_at', 'closed_at')

admin.site.register(TradeSession, TradeSessionAdmin)