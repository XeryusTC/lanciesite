from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
	name = models.CharField(max_length=255)
	start_date = models.DateField()
	end_date = models.DateField()
	registration_deadline = models.DateTimeField()

	def get_total_registrations(self):
		return self.participant_set.count()
	get_total_registrations.short_description = "Total registrations"

class Participant(models.Model):
	user = models.OneToOneField(User)

	address = models.CharField(max_length=255)
	telephone = models.CharField(max_length=15)
	iban = models.CharField(max_length=16)
	iban.verbose_name = "IBAN"
	city = models.CharField(max_length=255)

	transport = models.BooleanField()
	friday = models.BooleanField(default=True)
	saturday = models.BooleanField(default=True)
	sunday = models.BooleanField(default=True)

	event = models.ForeignKey(Event)

	def get_price(self):
		# TODO: calculate price of participation
		return 20
	get_price.short_description = "Price of participation"

	def __str__(self):
		return "{} ({})".format(self.user.get_full_name(), self.event.name)
