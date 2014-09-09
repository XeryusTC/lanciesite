from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from lanciesite.views import BaseStyleView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lanciesite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    url(r'^base_style.css$', BaseStyleView.as_view(), name="base_style"),
    url(r'^pos/', include('pointofsale.urls', namespace="pos")),
    url(r'^', include('pubsite.urls', namespace="pub")),
)
