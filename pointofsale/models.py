from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from pubsite.models import Participant, Event

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
    debit_id = models.SmallIntegerField(editable=False, default=lambda:get_next_debit_id())

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
        return self.participant.__str__()


class DrinkOrder(models.Model):
    account = models.ForeignKey(Account)
    drink = models.ForeignKey(Drink)
    time = models.DateTimeField(auto_now_add=True)
    cost = models.SmallIntegerField()

    class Meta:
        ordering = ["-time"]
        get_latest_by = "time"

    def save(self, *args, **kwargs):
        # Set the cost to the price of the drink by default
        if not self.cost:
            self.cost = self.drink.price
        super(DrinkOrder, self).save(*args, **kwargs)

    def __str__(self):
        return "[{1}] {2} - {0}".format(self.account, self.time, self.drink)


def get_next_debit_id():
    try:
        e = Event.objects.all()[0]
    except IndexError:
        # There is no event, but return a (semi-)useful value for the debit form anyway
        return 1

    try:
        a = Account.objects.filter(participant__event=e).order_by("-debit_id")[0]
        return a.debit_id + 1
    except IndexError:
        # No account for this event yet, return the first id
        return 1

