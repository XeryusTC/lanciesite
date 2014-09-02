from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.forms import Form, CharField, EmailField, BooleanField, Textarea, ValidationError, IntegerField

import string, random
from pubsite.models import Participant, get_price, get_current_event

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
    iban =         CharField(min_length=15, label="IBAN")
    email =        EmailField()

    friday = BooleanField(required=False)
    saturday = BooleanField(required=False)
    sunday = BooleanField(required=False)
    transport = BooleanField(label="Transport service", required=False)
    cover_member = BooleanField(label="Member of cover", required=False)
    pcs = IntegerField(initial=1, label="Amount of PCs or laptops")
    comment = CharField(widget=Textarea, required=False)

    def clean_postal_code(self):
        data = self.cleaned_data['postal_code']
        if not data[:4].isdigit() or not data[4:].isalpha():
            raise ValidationError("A postal code should be formatted XXXXYY where X is a number and Y is a letter")

        return data

    def clean_iban(self):
        # The following validation code has been based on http://rosettacode.org/wiki/IBAN#Python
        # remove spaces and convert to uppercase
        data = self.cleaned_data['iban'].upper().replace(' ', '')
        country2len = dict(AL=28, AD=24, AT=20, AZ=28, BE=16, BH=22, BA=20,
            BR=29, BG=22, CR=21, HR=21, CY=28, CZ=24, DK=18, DO=28, EE=20,
            FO=18, FI=18, FR=27, GE=22, DE=22, GI=23, GR=27, GL=18, GT=28,
            HU=28, IS=26, IE=22, IL=23, IT=27, KZ=20, KW=30, LV=21, LB=28,
            LI=21, LT=20, LU=20, MK=19, MT=31, MR=27, MU=30, MC=27, MD=24,
            ME=22, NL=18, NO=15, PK=24, PS=29, PL=28, PT=25, RO=24, SM=27,
            SA=24, RS=22, SK=24, SI=19, ES=24, SE=24, CH=21, TN=24, TR=26,
            AE=23, GB=22, VG=24)
        # validate length against the country code
        if data[:2] not in country2len or len(data) != country2len[data[:2]]:
            raise ValidationError("This is not a valid IBAN")

        # shift first 4 characters to the end and convert to base 36
        tmp = data[4:] + data[:4]
        converted = int(''.join(str(int(ch, 36)) for ch in tmp))
        if not converted % 97 == 1:
            raise ValidationError("This is not a valid IBAN")

        return data

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
        e = get_current_event()
        p = Participant(user=u, address=data['address'],
            postal_code=data['postal_code'], city=data['city'],
            telephone=data['phone_number'], iban=data['iban'],
            transport=data['transport'], friday=data['friday'],
            saturday=data['saturday'], sunday=data['sunday'], event=e,
            price=get_price(data['friday'], data['saturday'], data['sunday'], data['transport'], data['cover_member']),
            comment=data['comment'], pcs=data['pcs'])
        p.save()
        # TODO: send registration email
        return u

    def send_confirmation_mail(self):
        data = self.cleaned_data
        event = get_current_event()

        with open("pubsite/templates/pubsite/confirmation_mail.html") as fin:
            data_dict = {'event': event.name,
            'price': get_price(data['friday'], data['saturday'], data['sunday'], data['transport'], data['cover_member'])}
            data_dict.update(data)
            data_dict['friday'] = self.bool_to_human(data['friday'])
            data_dict['saturday'] = self.bool_to_human(data['saturday'])
            data_dict['sunday'] = self.bool_to_human(data['sunday'])
            data_dict['transport'] = self.bool_to_human(data['transport'])
            data_dict['cover_member'] = self.bool_to_human(data['cover_member']) # TODO: update this when updating model

            template = fin.read()
            message = string.Template(template)
            sender = "LanCie <" + settings.EMAIL_CONTACT_DESTINATION + ">"
            email = EmailMessage("{} registration".format(event), message.substitute(data_dict),
            sender, [data['email']], [sender])
            email.send()

    def bool_to_human(self, b):
        if b:
            return "Yes"
        return "No"
