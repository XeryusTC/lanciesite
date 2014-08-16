from django.contrib import admin
from pointofsale.models import Drink, DrinkOrder, Account

class DrinkAdmin(admin.ModelAdmin):
    fields = ('name', 'price')
    list_display = ('name', 'price', 'get_times_bought')

admin.site.register(Drink, DrinkAdmin)


class AccountAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('participant', 'credits')}),
        ('Statistics', {
            'classes': ('collapse'),
            'fields': ('get_drinks_bought', 'get_credits_used_on_drinks', 'get_credits_used', 'get_credits_remaining')
        }),
    )
    readonly_fields = ('get_drinks_bought', 'get_credits_used_on_drinks', 'get_credits_used', 'get_credits_remaining')
    list_display = ('__str__', 'credits', 'get_credits_used')

admin.site.register(Account, AccountAdmin)

class DrinkOrderAdmin(admin.ModelAdmin):
    list_display = ('time', 'drink', 'account', 'cost')
    list_filter = ('drink', 'account')

admin.site.register(DrinkOrder, DrinkOrderAdmin)
