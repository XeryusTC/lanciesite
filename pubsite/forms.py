from django.forms import Form, CharField, EmailField, BooleanField, Textarea

class ContactForm(Form):
    name = CharField(required=True)
    email = EmailField(required=True)
    subject = CharField(required=True)
    message = CharField(widget=Textarea)


class RegisterForm(Form):
    first_name =   CharField(required=True)
    last_name =    CharField(required=True)
    address =      CharField(required=True)
    postal_code =  CharField(required=True, max_length=6, min_length=6)
    city =         CharField(required=True)
    phone_number = CharField(required=True, max_length=15)
    iban =         CharField(required=True, max_length=16, label="IBAN")
    email =        EmailField(required=True)

    friday = BooleanField()
    saturday = BooleanField()
    sunday = BooleanField()
    transport = BooleanField(label="Transport service")
