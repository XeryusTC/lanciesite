from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.forms import Form, CharField, EmailField, BooleanField, Textarea

import string, random
from pubsite.models import Participant, Event

class ContactForm(Form):
    name = CharField()
    email = EmailField()
    subject = CharField()
    message = CharField(widget=Textarea)

    def send_mail(self):
        email = self.cleaned_data['email']
        sender = "{name} <{email}>".format(name=self.cleaned_data['name'], email=email)

        #TODO: use the actual lancie address here
        message = EmailMessage(self.cleaned_data['subject'], self.cleaned_data['message'],
            sender, [settings.EMAIL_CONTACT_DESTINATION], headers = {'Reply-To': email})
        message.send()


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

    def register(self):
        data = self.cleaned_data
        # Generate random username consisting of the first 8 letters of the last name + 8 random characters
        username = data['last_name'][:8] + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        # Create the contrib.auth User
        u = User.objects.create_user(username, data['email'], username) # use the username as the password
        u.first_name = data['first_name']
        u.last_name = data['last_name']
        u.save()
        # Create the participant using the latest event
        e = Event.objects.all()[0]
        p = Participant(user=u, address=data['address'],
            postal_code=data['postal_code'], city=data['city'],
            telephone=data['phone_number'], iban=data['iban'],
            transport=data['transport'], friday=data['friday'],
            saturday=data['saturday'], sunday=data['sunday'], event=e)
        p.save()
        # TODO: send registration email
        return u
