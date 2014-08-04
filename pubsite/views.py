from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
import json, string, random

from pubsite.forms import ContactForm, RegisterForm
from pubsite.models import get_price, Participant, Event

class AboutView(TemplateView):
    template_name = "pubsite/about.html"


class CompleteView(TemplateView):
    template_name = "pubsite/complete.html"


class ContactView(FormView):
    template_name = "pubsite/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('pub:thanks')

    def form_valid(self, form):
        # TODO: display an error message to the user
        try:
            form.send_mail()
        except:
            return HttpResponseRedirect(reverse('pub:contact'))
        return super(ContactView, self).form_valid(form)


class IndexView(TemplateView):
    template_name = "pubsite/index.html"


class CheckListView(TemplateView):
    template_name = "pubsite/checklist.html"


class RegisterView(FormView):
    template_name = "pubsite/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('pub:complete')

    def form_valid(self, form):
        data = form.cleaned_data
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
        # TODO: create pointofsale account
        # TODO: create debit forms (or possibly create these from a page in pointofsale)

        return super(RegisterView, self).form_valid(form)


class ThanksView(TemplateView):
    template_name = "pubsite/thanks.html"


class JSONResponseMixin():
    """
    A mixin that can be used to render a JSON response. Taken from the Django docs:
    https://docs.djangoproject.com/en/1.6/topics/class-based-views/mixins/#more-than-just-html
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class PriceJSONView(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get(self, request, friday, saturday, sunday, transport, *args, **kwargs):
        friday = self.var_to_boolean(friday)
        saturday = self.var_to_boolean(saturday)
        sunday = self.var_to_boolean(sunday)
        transport =  self.var_to_boolean(transport)

        return self.render_to_json_response({'price': get_price(friday, saturday, sunday, transport)})

    def var_to_boolean(self, var):
        """
        Responses are usually strings, but also handle integers. Returns False if argument is equal to 0, otherwise True.
        """
        if var == 0 or var == "0" or var.lower() == "false":
            return False
        return True
