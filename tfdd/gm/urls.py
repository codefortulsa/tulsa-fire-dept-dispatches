from django.conf.urls import url, patterns
# from django.views.generic.simple import direct_to_template



urlpatterns = patterns('gm.views',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^hydrants$', 'hydrant_map', name='hydrant_map'),

    url(r'^okdata$', 'okdata', name='okdata'),

    
    url(r'^(?P<tf_number>.*)/$', 'map_redirect', name='map_redirect'),

)


