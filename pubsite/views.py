from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
import json

from pubsite.forms import ContactForm, RegisterForm
from pubsite.models import get_price

class AboutView(TemplateView):
    template_name = "pubsite/about.html"


class CompleteView(TemplateView):
    template_name = "pubsite/complete.html"


class ContactView(FormView):
    template_name = "pubsite/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('pub:thanks')

    def form_valid(self, form):
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
