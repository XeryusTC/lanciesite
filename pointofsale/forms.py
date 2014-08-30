from django import forms
from pointofsale.models import Drink, Account

class BuyDrinkForm(forms.Form):
    account = forms.ChoiceField(required=True, widget=forms.RadioSelect)
    drink = forms.ChoiceField(required=True, widget=forms.RadioSelect)
