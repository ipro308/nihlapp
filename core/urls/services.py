from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/events/create$', 'nihlapp.core.views.services.events.create'),
    (r'^/events/delete$', 'nihlapp.core.views.services.events.delete'),
    (r'^/eventgoals/detail$', 'nihlapp.core.views.services.eventgoals.detail'),
    (r'^/eventgoals/create$', 'nihlapp.core.views.services.eventgoals.create'),
    (r'^/eventgoals/delete$', 'nihlapp.core.views.services.eventgoals.delete'),
    (r'^/eventpenalties/create$', 'nihlapp.core.views.services.eventpenalties.create'),
    (r'^/eventsuspensions/create$', 'nihlapp.core.views.services.eventsuspensions.create'),
    (r'^/eventgoalkeepersaves/create$', 'nihlapp.core.views.services.eventgoalkeepersaves.create'),
)