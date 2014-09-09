from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from pointofsale.models import Drink, Account, DrinkOrder
from pubsite.models import Participant, get_current_event, Event

class SaleView(TemplateView):
    template_name = "pointofsale/sale.html"
    success_url = reverse_lazy("pos:sale")
    insufficient = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SaleView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SaleView, self).get_context_data(**kwargs)

        # display an error if there was not enough money in the account to buy a drink
        context['insufficient'] = self.insufficient

        # get the current event or don't do anything if there is none
        try:
            event = get_current_event()
        except:
            return context

        context['drinks'] = Drink.objects.all()
        context['accounts'] = Account.objects.filter(participant__event=event)
        # get the last few drinks that have been bought during the event
        context['log'] = DrinkOrder.objects.filter(account__participant__event=event).order_by('-time')[:10]

        return context


class ParticipantOverview(TemplateView):
    template_name = "pointofsale/participants.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ParticipantOverview, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParticipantOverview, self).get_context_data(**kwargs)

        # get the latest event and its participants
        try:
            participant_list = Participant.objects.filter(event=get_current_event())

            # sort the participants according to whether they have an account or not
            context['not_finished'] = []
            context['finished'] = []
            for p in participant_list:
                try:
                    p.account
                except Account.DoesNotExist:
                    # participant doesn't have an account
                    context['not_finished'].append(p)
                else:
                    # participant does have an account
                    context['finished'].append(p)
        except IndexError:
            pass # return empty context

        return context


@login_required
def add_credits(request, participant):
    p = Participant.objects.get(pk=participant)
    try:
        p.account.credits += 5000
        p.account.save()
    except:
        # participant has no account yet so create it
        a = Account(participant=p, credits=5000)
        a.save()
    return HttpResponseRedirect(reverse("pos:participants"))

@login_required
def buy_drink(request, participant, drink, quantity):
    p = Participant.objects.get(pk=participant)
    d = Drink.objects.get(pk=drink)

    # Check if there is an actual account, and otherwise return nothing
    try:
        p.account
    except:
        return HttpResponseRedirect(reverse("pos:sale"))

    # Check if there are enough credits left
    if p.account.get_credits_remaining() < d.price:
        return HttpResponseRedirect(reverse("pos:sale_insufficient"))

    do = DrinkOrder.objects.create(account=p.account, drink=d)
    do.save()
    return HttpResponseRedirect(reverse("pos:sale"))
