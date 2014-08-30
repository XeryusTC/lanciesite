from django.conf.urls import patterns, url
from pubsite import views

urlpatterns = patterns('views',
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^checklist/$', views.CheckListView.as_view(), name='checklist'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^contact/thanks/$', views.ThanksView.as_view(), name='thanks'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^register/override/$', views.RegisterOverrideView.as_view(), name='register_override'),
    url(r'^register/complete/$', views.CompleteView.as_view(), name='complete'),
    url(r'^price/(?P<friday>\d+)/(?P<saturday>\d+)/(?P<sunday>\d+)/(?P<transport>\d+)/(?P<member>\d+)/$', views.PriceJSONView.as_view(), name='price'),
)
