from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()


urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^gm/', include('gm.urls')),
    url(r'^dispatches/', include('dispatches.urls')),
    url(r'^$', RedirectView.as_view(url='/dispatches/'))
)
