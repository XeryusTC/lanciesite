from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from pointofsale.models import Drink, Account, DrinkOrder
from pointofsale.forms import BuyDrinkForm
from pubsite.models import Participant, get_current_event


class BuyDrinkView(FormView):
    template_name = "pointofsale/buydrink.html"
    form_class = BuyDrinkForm
    success_url = reverse_lazy("pos:buy_drink")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuyDrinkView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BuyDrinkView, self).get_context_data(**kwargs)

        # get the list of available drinks
        context['all_drinks'] = Drink.objects.all()

        # get the list of all accounts for the ongoing event, first get the event
        try:
            event = get_current_event()
        except:
            return context

        context['all_accounts'] = {}
        for a in Account.objects.filter(participant__event=event):
            if a.get_credits_remaining() > 0:
                context['all_accounts'][a.pk] = {'credits': a.credits, 'used': a.get_credits_used(),
                    'remaining': a.get_credits_remaining(), 'name': a.participant.user.get_full_name() }

        # get the drinks that have been bought for the latest event
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
            pass

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
