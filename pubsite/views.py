from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

class AboutView(TemplateView):
    template_name = "pubsite/about.html"

class ContactView(FormView):
    template_name = "pubsite/contact.html"

class IndexView(TemplateView):
    template_name = "pubsite/index.html"

class CheckListView(TemplateView):
    template_name = "pubsite/checklist.html"

class RegisterView(FormView):
    template_name = "pubsite/register.html"

