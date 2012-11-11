from django.conf.urls import url, patterns

urlpatterns = patterns(
    'dispatches.views',

    url(r'^follow/(?P<unit_id>.*)/$', 'follow_unit',
        name='follow_unit'),
    url(r'^post/$', 'post', name='dispatch_post'),
    url(r'^$', 'index', name='responses_index'),
)
