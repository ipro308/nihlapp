from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Rink, EventType, Event, Season

@login_required
def upcoming(request):
    return render_to_response('core/schedule/upcoming.html', {'user': request.user})

@login_required
def recent(request):
    return render_to_response('core/schedule/recent.html', {'user': request.user})

@login_required
def matchups(request):
    return render_to_response('core/schedule/matchups.html', {'user': request.user})

@login_required
def create(request):
    
    rinks = Rink.objects.all()
    event_types = EventType.objects.filter(name = "Seeding Game")
    events = Event.objects.all().filter(homeTeam = request.user.get_profile().team, season = Season.objects.get(isCurrentSeason = True))
    
    return render_to_response('core/schedule/create.html', {'user': request.user, 'event_types': event_types, 'rinks': rinks, 'events': events})    