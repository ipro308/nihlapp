from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, EventType, Rink, Season, EventStatus
from time import strptime, strftime
from datetime import datetime

@login_required
def schedule(request):
    pass

def confirm(request):
    pass

def reject(request):
    pass

