from django.forms import Form, CharField, EmailField, BooleanField, Textarea

class ContactForm(Form):
    name = CharField()
    email = EmailField()
    subject = CharField()
    message = CharField(widget=Textarea)


class RegisterForm(Form):
    first_name =   CharField()
    last_name =    CharField()
    address =      CharField()
    postal_code =  CharField(max_length=6, min_length=6)
    city =         CharField()
    phone_number = CharField(max_length=15)
    iban =         CharField(max_length=16, label="IBAN")
    email =        EmailField()

    friday = BooleanField(required=False)
    saturday = BooleanField(required=False)
    sunday = BooleanField(required=False)
    transport = BooleanField(label="Transport service")
