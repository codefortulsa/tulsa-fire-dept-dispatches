from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dispatches/', include('dispatches.urls')),
    url(r'^send_text/', include('dispatches.urls')),
    url(r'^$', 'django.views.generic.simple.redirect_to',
        dict(url='/dispatches/', permanent=False)),
)
