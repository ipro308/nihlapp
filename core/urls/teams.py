# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import *
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Team
from nihlapp.core.views.teams import detail

urlpatterns = patterns('',
    (r'^/$', object_list,dict(queryset = Team.objects.all())),
    (r'^/detail/(?P<team_id>\d+)/?$', detail),
    (r'^/create/?$', 'nihlapp.core.views.teams.create_team'),
    (r'^/update/(?P<object_id>\d+)/?$', 'django.views.generic.create_update.update_object', 
	dict(model = Team, login_required = True)),
    (r'^/delete/(?P<object_id>\d+)/?$', 'django.views.generic.create_update.delete_object', 
	dict(model = Team, login_required = True, post_delete_redirect = "/teams")),
    (r'^/confirm/create/(?P<object_id>\d+)/?$', 'nihlapp.core.views.teams.confirm'),
    #(r'^/create/?$', 'django.views.generic.create_update.create_object',
    #dict(model = Team, login_required = True)),
    #(r'^/create/?$', 'nihlapp.core.views.teams.create_team'),
)
