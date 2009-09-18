from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/$', 'nihlapp.core.views.schedule.upcoming'),
    (r'^/recent$', 'nihlapp.core.views.schedule.recent'),
    (r'^/matchups$', 'nihlapp.core.views.schedule.matchups'),
)