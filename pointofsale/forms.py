from django import forms
from pointofsale.models import Drink, Account
from pubsite.models import Event

class BuyDrinkForm(forms.Form):
    account = forms.ChoiceField(required=True, widget=forms.RadioSelect)
    drink = forms.ChoiceField(required=True, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(BuyDrinkForm, self).__init__(*args, **kwargs)

        try:
            event = Event.objects.all()[0]
            self.fields['drink'].choices = ( (drink.pk, drink.pk) for drink in Drink.objects.all() )
            self.fields['account'].choices = ( (account.pk, account.pk) for account in Account.objects.filter(participant__event=event).order_by('participant__user__first_name') if account.get_credits_remaining() > 0)
        except:
            self.fields['drink'].choices = ()
            self.fields['account'].choices = ()
