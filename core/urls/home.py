from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/$', 'nihlapp.core.views.home.summary'),
    (r'^/deadlines$', 'nihlapp.core.views.home.deadlines'),
    (r'^/teams$', 'nihlapp.core.views.home.teams'),
)
