from django.contrib import admin
from pubsite.models import Event, Participant

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'registration_deadline']}),
        ('Weekend', {'fields': ['start_date', 'end_date']}),
        ('Other', {'fields': ['timelapse', 'description'], 'classes': ('collapse',)}),
    ]
    list_display = ('name', 'start_date', 'end_date', 'registration_deadline', 'get_total_registrations')
    search_fields = ['name']

admin.site.register(Event, EventAdmin)


class ParticipantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'event']}),
        ('Participation', {'fields': [('friday', 'saturday', 'sunday'), 'transport'], 'classes': ('collapse',)}),
        ('Address', {'fields': ['address', 'city'], 'classes': ('extrawide', 'collapse')}),
        ('Other', {'fields': ['telephone', 'iban'], 'classes': ('collapse',)}),
    ]
    list_display = ('__str__', 'friday', 'saturday', 'sunday', 'transport', 'get_price')
    list_filter = ('friday', 'saturday', 'sunday', 'transport', 'event')
    ordering = ('event__registration_deadline',)

admin.site.register(Participant, ParticipantAdmin)
