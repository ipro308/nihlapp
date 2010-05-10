from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Rink, EventType, Event, Season, EventGoal, EventStatus, Matchup
from django.db.models import Q

def upcoming(request):
    
    try:
        confirmedStatus = EventStatus.objects.get(name = "Confirmed")
        currentSeason = Season.objects.get(isCurrentSeason = True)
    except:
        return render_to_response('core/schedule/upcoming.html', {})
    
    # upcoming events (current season) (not completed)
    events = Event.objects.filter(eventStatus = confirmedStatus, season = currentSeason).order_by('dateTimeEvent')[:30]
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

@login_required
def matchups(request):
    
    currentSeason = Season.objects.get(isCurrentSeason = True)
    seedingGame = EventType.objects.get(name = "Seeding Game")
    seasonGame = EventType.objects.get(name = "Season Game")
    availableEvent = EventStatus.objects.get(name = "Available")
    scheduledEvent = EventStatus.objects.get(name = "Scheduled")
    confirmedEvent = EventStatus.objects.get(name = "Confirmed")
    completedEvent = EventStatus.objects.get(name = "Completed")
    userTeam = request.user.get_profile().team
    seasonStatus = currentSeason.seasonStatus
        
    # generate a list of seeding matchups with statuses
    seedingMatchups = list()
    qs = Matchup.objects.filter(Q(season = currentSeason) & 
                                Q(eventType = seedingGame) &
                                (Q(homeTeam = userTeam) | Q(awayTeam = userTeam))).order_by('homeTeam')
    for matchup in qs:
        matchupEntry = {}
        matchupEntry['matchup'] = matchup
        events = Event.objects.filter(season = currentSeason, 
                                      eventType = seedingGame, 
                                      homeTeam = matchup.homeTeam, 
                                      eventStatus = availableEvent)
        
        scheduled = Event.objects.filter(season = currentSeason, 
                                         eventType = seedingGame, 
                                         homeTeam = matchup.homeTeam, 
                                         awayTeam = matchup.awayTeam,                                         
                                         eventStatus = scheduledEvent,
                                         matchup = matchup)
    
        confirmed = Event.objects.filter(season = currentSeason, 
                                         eventType = seedingGame, 
                                         homeTeam = matchup.homeTeam, 
                                         awayTeam = matchup.awayTeam,
                                         eventStatus = confirmedEvent,
                                         matchup = matchup)
    
        completed = Event.objects.filter(season = currentSeason, 
                                         eventType = seedingGame, 
                                         homeTeam = matchup.homeTeam, 
                                         awayTeam = matchup.awayTeam,
                                         eventStatus = completedEvent,
                                         matchup = matchup)
    
        if len(scheduled) != 0:
            if scheduled[0].homeTeam == userTeam:
                matchupEntry['status'] = "requesthome"       
            else:
                matchupEntry['status'] = "requestaway"
            matchupEntry['event'] = scheduled[0]
        elif len(confirmed) != 0:
            matchupEntry['status'] = "confirmed"
            matchupEntry['event'] = confirmed[0]
        elif len(completed) != 0:
            matchupEntry['status'] = "completed"
        elif len(events) == 0:
            matchupEntry['status'] = "Waiting for home rink schedule."
        else:
            if matchup.awayTeam == userTeam:
                matchupEntry['status'] = "pickdate"
                matchupEntry['events'] = events
            else:
                matchupEntry['status'] = "Away team has not picked a date yet."
              
                
        seedingMatchups.append(matchupEntry)
        
    # generate a list of season matchups with statuses
    seasonMatchups = list()
    qs = Matchup.objects.filter(Q(season = currentSeason) & 
                                Q(eventType = seasonGame) &
                                (Q(homeTeam = userTeam) | Q(awayTeam = userTeam))).order_by('homeTeam')
    for matchup in qs:
        matchupEntry = {}
        matchupEntry['matchup'] = matchup
        events = Event.objects.filter(season = currentSeason, 
                                      eventType = seasonGame, 
                                      homeTeam = matchup.homeTeam, 
                                      eventStatus = availableEvent)
        
        scheduled = Event.objects.filter(season = currentSeason, 
                                         eventType = seasonGame, 
                                         homeTeam = matchup.homeTeam, 
                                         awayTeam = matchup.awayTeam,                                         
                                         eventStatus = scheduledEvent,
                                         matchup = matchup)
    
        confirmed = Event.objects.filter(season = currentSeason, 
                                         eventType = seasonGame, 
                                         homeTeam = matchup.homeTeam, 
                                         awayTeam = matchup.awayTeam,
                                         eventStatus = confirmedEvent,
                                         matchup = matchup)
    
        completed = Event.objects.filter(season = currentSeason, 
                                         eventType = seasonGame, 
                                         homeTeam = matchup.homeTeam, 
                                         awayTeam = matchup.awayTeam,
                                         eventStatus = completedEvent,
                                         matchup = matchup)
    
        if len(scheduled) != 0:
            if scheduled[0].homeTeam == userTeam:
                matchupEntry['status'] = "requesthome"       
            else:
                matchupEntry['status'] = "requestaway"
            matchupEntry['event'] = scheduled[0]
        elif len(confirmed) != 0:
            matchupEntry['status'] = "confirmed"
            matchupEntry['event'] = confirmed[0]
        elif len(completed) != 0:
            matchupEntry['status'] = "completed"
        elif len(events) == 0:
            matchupEntry['status'] = "Waiting for home rink schedule."
        else:
            if matchup.awayTeam == userTeam:
                matchupEntry['status'] = "pickdate"
                matchupEntry['events'] = events
            else:
                matchupEntry['status'] = "Away team has not picked a date yet."
              
                
        seasonMatchups.append(matchupEntry)
    
    return render_to_response('core/schedule/matchups.html', {'user': request.user,
                                                              'seedingMatchups': seedingMatchups,
                                                              'seasonMatchups': seasonMatchups,
                                                              'seasonStatus': seasonStatus,
                                                              'currentSeason': currentSeason})

@login_required
def create(request):
    
    currentSeason = Season.objects.get(isCurrentSeason = True)
    rinks = Rink.objects.all()
    
    if currentSeason.seasonStatus.name == "Scheduling Seeding Games":
        event_types = EventType.objects.filter(name = "Seeding Game")
    elif currentSeason.seasonStatus.name == "Scheduling Season Games":
        event_types = EventType.objects.filter(name = "Season Game")
    else:
        event_types = EventType.objects.filter(name = "Practice Game")
        
    events = Event.objects.all().filter(homeTeam = request.user.get_profile().team, season = Season.objects.get(isCurrentSeason = True)).order_by('-id')
    
    return render_to_response('core/schedule/create.html', {'user': request.user, 
                                                            'event_types': event_types, 
                                                            'rinks': rinks, 
                                                            'events': events})

    