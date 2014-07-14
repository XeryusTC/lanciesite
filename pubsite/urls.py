from django.conf.urls import patterns, url
from pubsite import views

urlpatterns = patterns('views',
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^checklist/$', views.CheckListView.as_view(), name='checklist'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
)
