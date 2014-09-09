from django.conf.urls import patterns, url
from pointofsale import views

urlpatterns = patterns('',
    url(r'^$', views.SaleView.as_view(), name="sale"),
    url(r'^participants/$', views.ParticipantOverview.as_view(), name="participants"),
    url(r'^add_credits/(?P<participant>\d+)/$', views.add_credits, name="add_credits"),
)
