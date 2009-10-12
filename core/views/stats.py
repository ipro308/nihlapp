from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Event, Season, EventStatus

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

@login_required
def record(request):
    events = Event.objects.all().filter(eventStatus = EventStatus.objects.get(name = "Completed"), homeTeam = request.user.get_profile().team, season = Season.objects.get(isCurrentSeason = True))
    return render_to_response('core/stats/record.html', {'user': request.user, 'events': events})

@login_required
def event(request, object_id):
    
    return render_to_response('core/stats/event.html', {'user': request.user, 'event': Event.objects.get(id = object_id)})
