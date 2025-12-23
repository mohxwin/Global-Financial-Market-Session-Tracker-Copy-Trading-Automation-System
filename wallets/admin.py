from django.contrib import admin
from .models import CoinWallet

# Register your models here.
class CoinWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at', 'updated_at')
    search_fields = ('user__username', )
    
admin.site.register(CoinWallet, CoinWalletAdmin)