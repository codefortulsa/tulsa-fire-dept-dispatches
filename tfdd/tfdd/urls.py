from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(''
    # Examples:
    # url(r'^$', 'tfdd.views.home', name='home'),
    # url(r'^tfdd/', include('tfdd.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    ,url(r'^admin/', include(admin.site.urls))
    ,url(r'^dispatches/', include('dispatches.urls'))
    ,url(r'^send_text/',include('dispatches.urls'))
    ,url(r'^unit_select/',include('dispatches.urls'))


)
