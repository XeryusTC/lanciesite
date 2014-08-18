from django.conf.urls import patterns, url
from pointofsale import views

urlpatterns = patterns('',
    url(r'^$', views.BuyDrinkView.as_view(), name="buydrink"),
)
