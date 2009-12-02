from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from nihlapp.core.models import Team, Season, Event, EventStatus, EventGoal, EventType
from datetime import datetime

def summary(request):
    
    completedStatus = EventStatus.objects.get(name = "Completed")
    currentSeason = Season.objects.get(isCurrentSeason = True)
    
    # recent events (current season) (completed)
    events = Event.objects.filter(eventStatus = completedStatus, season = currentSeason).order_by('-dateTimeEvent')[:20]
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
    
    completed = EventStatus.objects.get(name = 'Completed')
    currentSeason = Season.objects.get(isCurrentSeason = True)
    numTeams = Team.objects.filter(season = currentSeason).count()
    numGames = Event.objects.filter(Q(season = currentSeason) & Q(eventStatus = completed)).count()
    
    # generate reminders
    reminders = []
    if request.user.is_authenticated():
        # user needs to enter rink schedule
        if currentSeason.seasonStatus.name == "Scheduling Seeding Games":
            eventType = EventType.objects.get(name = "Seeding Game")
            events = Event.objects.filter(season = currentSeason, 
                                          eventType = eventType, 
                                          homeTeam = request.user.get_profile().team)
            if len(events) == 0:
                reminders.append({'url': '/schedule/create', 'note': 'Enter home rink schedule for seeding games'})
                
        if currentSeason.seasonStatus.name == "Scheduling Season Games":
            eventType = EventType.objects.get(name = "Season Game")
            events = Event.objects.filter(season = currentSeason, 
                                          eventType = eventType, 
                                          homeTeam = request.user.get_profile().team)
            if len(events) == 0:
                reminders.append({'url': '/schedule/create', 'note': 'Enter home rink schedule for season games'})
        
        # user needs to accept or reject requests
        scheduledStatus = EventStatus.objects.get(name = "Scheduled")
        events = Event.objects.filter(eventStatus = scheduledStatus, 
                                      homeTeam = request.user.get_profile().team)
        if len(events) > 0:
            reminders.append({'url': '/schedule/matchups', 'note': 'Confirm or Reject game scheduling requests'})
            
        # user needs to enter stats
        confirmedStatus = EventStatus.objects.get(name = "Confirmed")
        events = Event.objects.filter(eventStatus = confirmedStatus, 
                                      dateTimeEvent__lt = datetime.now(),
                                      homeTeam = request.user.get_profile().team)
        if len(events) > 0:
            reminders.append({'url': '/stats/record', 'note': 'Enter game statistics'})
    
    return render_to_response('core/home/summary.html', {'user': request.user, 
                                                         'currentSeason': currentSeason,
                                                         'numTeams': numTeams,
                                                         'numGames': numGames,
                                                         'events': eventList,
                                                         'reminders': reminders})

def deadlines(request):
    return render_to_response('core/home/deadlines.html', {'user': request.user, 
                                                           'currentSeason': Season.objects.get(isCurrentSeason = True)})

def teams(request):
    teams = Team.objects.order_by('name')
    return render_to_response('core/home/teams.html', {'user': request.user, 'teams': teams})
