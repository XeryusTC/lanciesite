from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from pubsite.forms import ContactForm, RegisterForm

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

