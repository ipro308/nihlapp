from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/events/detail$', 'nihlapp.core.views.services.events.detail'),
    (r'^/events/create$', 'nihlapp.core.views.services.events.create'),
    (r'^/events/delete$', 'nihlapp.core.views.services.events.delete'),
    (r'^/eventgoals/detail$', 'nihlapp.core.views.services.eventgoals.detail'),
    (r'^/eventgoals/create$', 'nihlapp.core.views.services.eventgoals.create'),
    (r'^/eventgoals/delete$', 'nihlapp.core.views.services.eventgoals.delete'),
    (r'^/eventpenalties/detail$', 'nihlapp.core.views.services.eventpenalties.detail'),
    (r'^/eventpenalties/create$', 'nihlapp.core.views.services.eventpenalties.create'),
    (r'^/eventpenalties/delete$', 'nihlapp.core.views.services.eventpenalties.delete'),
    (r'^/eventsuspensions/detail$', 'nihlapp.core.views.services.eventsuspensions.detail'),
    (r'^/eventsuspensions/create$', 'nihlapp.core.views.services.eventsuspensions.create'),
    (r'^/eventsuspensions/delete$', 'nihlapp.core.views.services.eventsuspensions.delete'),
    (r'^/eventgoalkeepersaves/detail$', 'nihlapp.core.views.services.eventgoalkeepersaves.detail'),
    (r'^/eventgoalkeepersaves/create$', 'nihlapp.core.views.services.eventgoalkeepersaves.create'),
    (r'^/eventgoalkeepersaves/delete$', 'nihlapp.core.views.services.eventgoalkeepersaves.delete'),
)