from django.conf.urls import url, patterns

urlpatterns = patterns(
    'dispatches.views',
    url(r'^send_text/','send_text'),
    url(r'^follow/(?P<unit_id>.*)/$', 'follow_unit',
        name='follow_unit'),
    url(r'^post/$', 'post', name='dispatch_post'),
    url(r'^register/$', 'register', name='dispatches_register'),
    url(r'^$', 'index', name='dispatches'),
)
