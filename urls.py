from django.conf.urls.defaults import *
from django.conf import settings
#from django.contrib.comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import *
from django.views.generic.list_detail import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    # static content
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_DOC_ROOT}),

    # authentication and account management
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^accounts/password_reset_done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^accounts/password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^accounts', include('nihlapp.core.urls.accounts')),

    # generic views for models
    (r'^teams', include('nihlapp.core.urls.teams')),
    (r'^clubs', include('nihlapp.core.urls.clubs')),
    (r'^divisions', include('nihlapp.core.urls.divisions')),
    (r'^rinks', include('nihlapp.core.urls.rinks')),
    (r'^seasons', include('nihlapp.core.urls.seasons')),
    (r'^parameter', include('nihlapp.core.urls.parameter')),
    
    # home module
    (r'^home', include('nihlapp.core.urls.home')),

    # stats module
    (r'^stats', include('nihlapp.core.urls.stats')),

    # schedule module
    (r'^schedule', include('nihlapp.core.urls.schedule')),
  
    # index
    (r'^$', 'nihlapp.core.views.home.summary'),
)
