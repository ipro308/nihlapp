# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import *


urlpatterns = patterns('',
    (r'^/$', login_required(object_list), 
        dict(queryset = User.objects.all())),
				#(r'^/create/?$', 'django.views.generic.create_update.create_object', dict(model = User, login_required = True, post_save_redirect='/accounts/confirm/create/%{object_id)s/')),
    (r'^/detail/(?P<object_id>\d+)/?$', 'django.views.generic.list_detail.object_detail', 
        dict(queryset = User.objects.all())),
    (r'^/delete/(?P<object_id>\d+)/?$', 'django.views.generic.create_update.delete_object',
        dict(model = User, login_required = True, post_delete_redirect = "/")),
				(r'^/confirm/create/(?P<object_id>\d+)/?$', 'nihlapp.core.views.accounts.confirm'),
)
