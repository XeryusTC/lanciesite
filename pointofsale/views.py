import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView
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
        except Event.DoesNotExist:
            pass # return empty context

        return context


class BuyDrinkRedirectView(RedirectView):
    pattern_name = "pos:sale"
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuyDrinkRedirectView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, participant, drink, quantity, *args, **kwargs):
        try:
            buy_drink(participant, drink, quantity)
        except InsufficientFundsException:
            self.pattern_name = "pos:sale_insufficient"
        except Account.DoesNotExist:
            # someone tried to buy something for an account which does not exist
            # let it slide for now, but TODO: handle this gracefully
            pass
        return super(BuyDrinkRedirectView, self).get_redirect_url(*args, **kwargs)


class AddCreditsRedirectView(RedirectView):
    pattern_name = "pos:participants"
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddCreditsRedirectView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, participant, *args, **kwargs):
        p = Participant.objects.get(pk=participant)
        try:
            p.account.credits += 5000
            p.account.save()
        except:
            a = Account(participant=p, credits=5000)
            a.save()
        return super(AddCreditsRedirectView, self).get_redirect_url(*args, **kwargs)


class GenerateCSVView(TemplateView):
    template_name = "pointofsale/csv.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenerateCSVView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GenerateCSVView, self).get_context_data(**kwargs)

        context['csv'] = "id,amount,name,address,place,IBAN,email,date\n"

        try:
            e = get_current_event()
            participants = Participant.objects.filter(event=e).order_by('account__debit_id')
            for p in participants:
                try:
                    id = p.account.debit_id
                    context['csv'] += """{id},{amount},"{name}","{address}","{place}","{iban}","{email}",{date}\n""".format(
                        id=id*2-1, amount=p.price, name=p.user.get_full_name(),
                        address=p.address + " " + p.postal_code, place=p.city,
                        iban=p.iban, email=p.user.email, date=e.start_date)
                    context['csv'] += """{id},{amount},"{name}","{address}","{place}","{iban}","{email}",{date}\n""".format(
                        id=id*2, amount=p.account.get_credits_used()/100.0, name=p.user.get_full_name(),
                        address=p.address + " " + p.postal_code, place=p.city,
                        iban=p.iban, email=p.user.email, date=e.end_date)
                except:
                    # Nothing to do here, the participant doesn't have any costs so it shouldn't be reported in the csv
                    pass
        except Event.DoesNotExist:
            return context # There are no events so there is no CSV to be generated

        return context

    def render_to_response(self, context, **kwargs):
        return super(TemplateView, self).render_to_response(context, content_type="text/plain", **kwargs) # override the MIME type


class InsufficientFundsException(Exception):
    pass


def buy_drink(participant, drink, quantity):
    p = Participant.objects.get(pk=participant)
    d = Drink.objects.get(pk=drink)
    quantity = int(quantity)

    if p.account.get_credits_remaining() < d.price * quantity:
        raise InsufficientFundsException()

    for i in range(quantity):
        do = DrinkOrder.objects.create(account=p.account, drink=d)
        do.save()
