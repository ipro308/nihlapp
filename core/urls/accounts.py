from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import *

urlpatterns = patterns('',
    (r'^/$', login_required(object_list), 
        dict(queryset = User.objects.all(), paginate_by = 20)),
    (r'^/detail/(?P<object_id>\d+)/?$', 'django.views.generic.list_detail.object_detail', 
        dict(queryset = User.objects.all())),        
)
