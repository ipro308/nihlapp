from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def summary(request):
    return render_to_response('core/stats/summary.html', {'user': request.user})

@login_required
def seeding(request):
    return render_to_response('core/stats/seeding.html', {'user': request.user})

@login_required
def season(request):
    return render_to_response('core/stats/season.html', {'user': request.user})

@login_required
def playoffs(request):
    return render_to_response('core/stats/playoffs.html', {'user': request.user})

@login_required
def tournament(request):
    return render_to_response('core/stats/tournament.html', {'user': request.user})
