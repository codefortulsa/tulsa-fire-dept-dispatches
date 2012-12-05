from django.conf.urls import url, patterns
from django.views.generic.simple import direct_to_template

urlpatterns = patterns(
    'dispatches.views',

    url(r'^unit_select/','unit_select'),
    url(r'^follow/(?P<unit_id>.*)/(?P<channel>.*)/(?P<state>.*)/$', 'follow_unit',
        name='follow_unit'),
    url(r'^post/$', 'post', name='dispatch_post'),
    url(r'^register/$', 'register', name='dispatches_register'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^following/$', 'following', name='following'),
    url(r'^unit_detail/(?P<unit_id>.*)/$', 'unit_detail', name='unit_detail'),
    url(r'^update_check/(?P<start_tf>.*)/(?P<dispatch_filter>.*)/$', 'check_for_update',name='check_for_update'),
    
    url(r'^by_tf/(?P<start_tf>.*)/(?P<how_many>.*)/(?P<dispatch_filter>.*)/$', 'dispatch_list',name='dispatch_list'),
    url(r'^settings/$', 'update_settings', name='settings'),
    url(r'^register/phone/$', 'register_phone', name='register_phone'),
    url(r'^register/email/$', 'register_email', name='register_email'),
    url(r'^about/$', 'about',name='about'),
    url(r'^$', 'index', name='dispatches'),
    
)
