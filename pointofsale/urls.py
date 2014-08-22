from django.conf.urls import patterns, url
from pointofsale import views

urlpatterns = patterns('',
    url(r'^$', views.BuyDrinkView.as_view(), name="buydrink"),
    url(r'^participants/$', views.ParticipantOverview.as_view(), name="participants"),
)
