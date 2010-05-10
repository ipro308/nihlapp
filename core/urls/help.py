from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/$', 'nihlapp.core.views.help.help'),
    (r'^/faq$', 'nihlapp.core.views.help.faq'),
)
