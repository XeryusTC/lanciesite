from django.db import models
from django.contrib.auth.models import User
from pubsite.models import Participant
from django.core.urlresolvers import reverse

class Drink(models.Model):
    name = models.CharField(max_length=32)
    price = models.SmallIntegerField()

    def get_times_bought(self):
        return self.drinkorder_set.count()
    get_times_bought.short_description = "Times bought"

    def __str__(self):
        return self.name


class Account(models.Model):
    participant = models.OneToOneField(Participant)

    credits = models.IntegerField(default=0)

    drinks_bought = models.ManyToManyField(Drink, through='DrinkOrder')

    def get_absolute_url(self):
        pass

    def get_drinks_bought(self):
        return self.drinkorder_set.count()
    get_drinks_bought.short_description = "Total drinks bought"

    def get_credits_used_on_drinks(self):
        # TODO: implement
        return 0
    get_credits_used_on_drinks.short_description = "Credits used for drinks"

    def get_credits_used(self):
        return self.get_credits_used_on_drinks()
    get_credits_used.short_description = "Credits used"

    def get_credits_remaining(self):
        return self.credits - self.get_credits_used()
    get_credits_remaining.short_description = "Credits remaining"

    def __str__(self):
        return self.participant.user.get_full_name()


class DrinkOrder(models.Model):
    account = models.ForeignKey(Account)
    drink = models.ForeignKey(Drink)
    time = models.DateTimeField(auto_now_add=True)
    cost = models.SmallIntegerField()

    class Meta:
        ordering = ["-time"]
        get_latest_by = "time"

    def __str__(self):
        return "[{1}] {2} - {0}".format(self.account, self.time, self.drink)
