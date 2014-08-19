from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.views.generic.base import ContextMixin
import json, datetime, smtplib

from pubsite.forms import ContactForm, RegisterForm
from pubsite.models import get_price, Event

class EventTitleMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(EventTitleMixin, self).get_context_data(**kwargs)
        event = Event.objects.all()[0]
        context['event_title'] = event

        if event.end_date < datetime.date.today(): # the last event has already passed
            context['current_event'] = None
            context['past_events'] = Event.objects.all()[:5]
        else:
            context['current_event'] = event
            context['past_events'] = Event.objects.all()[1:6]
        return context

class AboutView(EventTitleMixin, TemplateView):
    template_name = "pubsite/about.html"


class CompleteView(EventTitleMixin, TemplateView):
    template_name = "pubsite/complete.html"


class ContactView(EventTitleMixin, FormView):
    template_name = "pubsite/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('pub:thanks')

    def form_valid(self, form):
        try:
            form.send_mail()
        except:
            form.errors[NON_FIELD_ERRORS] = form.error_class(['Could not send the email, please try again later'])
            return super(ContactView, self).form_invalid(form)
        return super(ContactView, self).form_valid(form)


class IndexView(EventTitleMixin, TemplateView):
    template_name = "pubsite/index.html"


class CheckListView(EventTitleMixin, TemplateView):
    template_name = "pubsite/checklist.html"


class RegisterView(EventTitleMixin, FormView):
    template_name = "pubsite/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('pub:complete')

    def form_valid(self, form):
        form.register()
        try:
            form.send_confirmation_mail()
        except smtplib.SMTPException:
            form.errors[NON_FIELD_ERRORS] = form.error_class(["Could not send confirmation email but you should be registered. When in doubt please send a mail to lancie@svcover.nl"])
            return super(RegisterView, self).form_invalid(form)
        # TODO: create pointofsale account
        # TODO: create debit forms (or possibly create these from a page in pointofsale)

        return super(RegisterView, self).form_valid(form)


class ThanksView(EventTitleMixin, TemplateView):
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

    def get(self, request, friday, saturday, sunday, transport, member, *args, **kwargs):
        friday = self.var_to_boolean(friday)
        saturday = self.var_to_boolean(saturday)
        sunday = self.var_to_boolean(sunday)
        transport =  self.var_to_boolean(transport)
        member = self.var_to_boolean(member)

        return self.render_to_json_response({'price': get_price(friday, saturday, sunday, transport, member)})

    def var_to_boolean(self, var):
        """
        Responses are usually strings, but also handle integers. Returns False if argument is equal to 0, otherwise True.
        """
        if var == 0 or var == "0" or var.lower() == "false":
            return False
        return True
