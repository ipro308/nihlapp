from django.conf.urls.defaults import *
from django.views.generic.list_detail import *
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Club
from nihlapp.core.views.clubs import detail

urlpatterns = patterns('',
    (r'^/$', object_list, 
        dict(queryset = Club.objects.all())),
    (r'^/detail/(?P<object_id>\d+)/?$', detail),
    (r'^/create/?$', 'django.views.generic.create_update.create_object', 
        dict(model = Club, login_required = True)),
    (r'^/update/(?P<object_id>\d+)/?$', 'django.views.generic.create_update.update_object', 
        dict(model = Club, login_required = True)),
    (r'^/delete/(?P<object_id>\d+)/?$', 'django.views.generic.create_update.delete_object', 
        dict(model = Club, login_required = True, post_delete_redirect = "/clubs")),
)
	
