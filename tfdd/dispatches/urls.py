from django.conf.urls import url, patterns

urlpatterns = patterns(
    'dispatches.views',

    url(r'^follow','follow_unit'),

    url(r'^$', 'index'), 
)
