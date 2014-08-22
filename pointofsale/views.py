from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from pointofsale.models import Drink, Account, DrinkOrder
from pointofsale.forms import BuyDrinkForm
from pubsite.models import Event, Participant


class BuyDrinkView(FormView):
    template_name = "pointofsale/buydrink.html"
    form_class = BuyDrinkForm
    success_url = reverse_lazy("pos:buy_drink")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuyDrinkView, self).dispatch(*args, **kwargs)


class ParticipantOverview(TemplateView):
    template_name = "pointofsale/participants.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ParticipantOverview, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParticipantOverview, self).get_context_data(**kwargs)

        # get the latest event and its participants
        try:
            e = Event.objects.all()[0]
            participant_list = Participant.objects.filter(event=e)

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
