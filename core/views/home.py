from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Team

@login_required
def summary(request):
    return render_to_response('core/home/summary.html', {'user': request.user})

@login_required
def deadlines(request):
    return render_to_response('core/home/deadlines.html', {'user': request.user})

@login_required
def teams(request):
    object_list = Team.objects.order_by('name')
    return render_to_response('core/home/teams.html', {'user': request.user, 'object_list': object_list})
