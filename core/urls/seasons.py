# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import *
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Season

urlpatterns = patterns('',
    (r'^/$', object_list, dict(queryset = Season.objects.all())),
       (r'^/detail/(?P<object_id>\d+)/?$', object_detail, 
        dict(queryset = Season.objects.all())),
    (r'^/create/?$', 'django.views.generic.create_update.create_object', 
        dict(model = Season, login_required = True, post_save_redirect='/seasons/confirm/create/%(object_id)s/')),
    (r'^/update/(?P<object_id>\d+)/?$', 'django.views.generic.create_update.update_object', 
        dict(model = Season, login_required = True)),
    (r'^/stage1$', 'nihlapp.core.views.seasons.stage1'),
    (r'^/stage2$', 'nihlapp.core.views.seasons.stage2'),
    (r'^/stage3$', 'nihlapp.core.views.seasons.stage3'),
    (r'^/stage4$', 'nihlapp.core.views.seasons.stage4'),
    (r'^/stage5$', 'nihlapp.core.views.seasons.stage5'),
    (r'^/confirm/create/(?P<object_id>\d+)/?$', 'nihlapp.core.views.seasons.confirm'),
)
