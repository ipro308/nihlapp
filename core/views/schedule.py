from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Rink, EventType, Event, Season, EventGoal, EventStatus

def upcoming(request):
    
    completedStatus = EventStatus.objects.get(name = "Completed")
    currentSeason = Season.objects.get(isCurrentSeason = True)
    
    # upcoming events (current season) (not completed)
    events = Event.objects.filter(eventStatus__lt = completedStatus, season = currentSeason).order_by('dateTimeEvent')[:30]
    eventList = list()
    for object in events:
        eventList.append({'id': object.id,
                               'homeTeam': object.homeTeam,
                               'awayTeam': object.awayTeam,
                               'eventType': object.eventType,
                               'dateTimeEvent': object.dateTimeEvent,
                               'rink': object.rink,
                               'eventStatus': object.eventStatus})    
    
    return render_to_response('core/schedule/upcoming.html', {'user': request.user, 'events': eventList})

def recent(request):
    
    completedStatus = EventStatus.objects.get(name = "Completed")
    currentSeason = Season.objects.get(isCurrentSeason = True)
    
    # recent events (current season) (completed)
    events = Event.objects.filter(eventStatus = completedStatus, season = currentSeason).order_by('-dateTimeEvent')[:30]
    eventList = list()
    for object in events:
        homeGoals = EventGoal.objects.filter(event = object, team = object.homeTeam).count()
        awayGoals = EventGoal.objects.filter(event = object, team = object.awayTeam).count()
        eventList.append({'id': object.id,
                               'homeTeam': object.homeTeam,
                               'awayTeam': object.awayTeam,
                               'eventType': object.eventType,
                               'dateTimeEvent': object.dateTimeEvent,
                               'rink': object.rink,
                               'eventStatus': object.eventStatus,
                               'score': "%s:%s" % (homeGoals, awayGoals)})    
    
    return render_to_response('core/schedule/recent.html', {'user': request.user, 'events': eventList})

def matchups(request):
    return render_to_response('core/schedule/matchups.html', {'user': request.user})

@login_required
def create(request):
    
    rinks = Rink.objects.all()
    event_types = EventType.objects.filter(name = "Seeding Game")
    events = Event.objects.all().filter(homeTeam = request.user.get_profile().team, season = Season.objects.get(isCurrentSeason = True)).order_by('-id')
    
    return render_to_response('core/schedule/create.html', {'user': request.user, 'event_types': event_types, 'rinks': rinks, 'events': events})    