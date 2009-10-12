from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/events/create$', 'nihlapp.core.views.services.events.create'),
)