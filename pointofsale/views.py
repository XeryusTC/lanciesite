from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from pointofsale.models import Drink, Account, DrinkOrder
from pointofsale.forms import BuyDrinkForm


class BuyDrinkView(FormView):
    template_name = "pointofsale/buydrink.html"
    form_class = BuyDrinkForm
    success_url = reverse_lazy("pos:buy_drink")

class ParticipantOverview(TemplateView):
    template_name = "pointofsale/participants.html"
