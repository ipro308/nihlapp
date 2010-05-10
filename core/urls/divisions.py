from django.conf.urls.defaults import *
from django.views.generic.list_detail import *
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Division
from nihlapp.core.views.divisions import detail

urlpatterns = patterns('',
    (r'^/$', object_list, 
        dict(queryset = Division.objects.all())),
    (r'^/detail/(?P<object_id>\d+)/?$', detail),
    (r'^/create/?$', 'django.views.generic.create_update.create_object', 
        dict(model = Division, login_required = True, post_save_redirect='/divisions/confirm/create/%(object_id)s/')),
    (r'^/update/(?P<object_id>\d+)/?$', 'django.views.generic.create_update.update_object', 
        dict(model = Division, login_required = True)),
    (r'^/delete/(?P<object_id>\d+)/?$', 'django.views.generic.create_update.delete_object', 
        dict(model = Division, login_required = True, post_delete_redirect = "/divisions")),
		(r'^/confirm/create/(?P<object_id>\d+)/?$', 'nihlapp.core.views.divisions.confirm'),
)
