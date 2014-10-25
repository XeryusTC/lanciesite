from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    timelapse = models.CharField(blank=True, max_length=255)
    photo_book_id = models.IntegerField(blank=True, null=True)

    # date information
    start_date = models.DateField()
    end_date = models.DateField()
    registration_deadline = models.DateTimeField()

    def get_total_registrations(self):
        return self.participant_set.count()
    get_total_registrations.short_description = "Total registrations"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-start_date"]
        get_latest_by = "start_date"


class Participant(models.Model):
    user = models.OneToOneField(User)

    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    iban = models.CharField(max_length=255)
    iban.verbose_name = "IBAN"

    # The following affect the price
    transport = models.BooleanField(default=False)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)
    cover_member = models.BooleanField(default=True)
    price = models.SmallIntegerField()

    event = models.ForeignKey(Event)
    pcs = models.SmallIntegerField(default=1)
    comment = models.TextField(default="")


    def get_price(self):
        return get_price(self.friday, self.saturday, self.sunday, self.transport, self.cover_member)
    get_price.short_description = "Price"

    def __str__(self):
        return "{} ({})".format(self.user.get_full_name(), self.event.name)


def get_price(friday, saturday, sunday, transport, member):
    price = 20
    # only present one or two days
    if not (friday and saturday and sunday) and not (friday and saturday) and not (friday and sunday) and not (saturday and sunday):
        price = 15
    # not present any of the days/no entry fee (BHV for example don't pay an entry fee)
    if not friday and not saturday and not sunday:
        price = 0
    if transport:
        price += 5
    if not member:
        price += 5
    return price

def get_current_event():
    return Event.objects.latest()
