from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def upcoming(request):
    return render_to_response('core/schedule/upcoming.html', {'user': request.user})

@login_required
def recent(request):
    return render_to_response('core/schedule/recent.html', {'user': request.user})

@login_required
def matchups(request):
    return render_to_response('core/schedule/matchups.html', {'user': request.user})
