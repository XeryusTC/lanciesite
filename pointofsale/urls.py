from django.conf.urls import patterns, url
from pointofsale import views

urlpatterns = patterns('',
    url(r'^$', views.SaleView.as_view(), name="sale"),
    url(r'^insufficient/$', views.SaleView.as_view(insufficient=True), name="sale_insufficient"),
    url(r'^participants/$', views.ParticipantOverview.as_view(), name="participants"),
    url(r'^add_credits/(?P<participant>\d+)/$', views.add_credits, name="add_credits"),
    url(r'^buy_drink/(?P<participant>\d+)/(?P<drink>\d+)/(?P<quantity>\d+)/$', views.BuyDrinkRedirectView.as_view(), name="buy_drink"),
)
