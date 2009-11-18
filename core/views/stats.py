from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Event, Season, EventStatus, Team, PenaltyOffense, EventGoal, EventPenalty, EventSuspension, EventGoalkeeperSaves, EventStats, Parameter, EventType, Division, SkillLevel, Club
from nihlapp.core.utils import TeamStats
from django.db.models import Q
from datetime import datetime, timedelta

def summary(request):
    # variables
    url = request.get_full_path()
    
    # dictionaries
    teams = TeamStats.objects.filter(season = Season.objects.get(isCurrentSeason = True))
    stats = list()
    divisions = Division.objects.all()
    levels = SkillLevel.objects.all()
    clubs = Club.objects.all()
    
    # initialize filters
    division_filter = []
    level_filter = []
    club_filter = []
    team_filter = []
    
    # begin populating filters
    # if filter was not selected, 
    # it will be set to a list with a string of the number zero

    if len(request.GET.getlist('division')) == 0:
        division_filter = [0]
    for i in request.GET.getlist('division'):
        division_filter.append(int(i))
    
    if len(request.GET.getlist('level')) == 0:
        level_filter = [0]
    for i in request.GET.getlist('level'):
        level_filter.append(int(i))

    if len(request.GET.getlist('club')) == 0:
        club_filter = [0]
    for i in request.GET.getlist('club'):
        club_filter.append(int(i))
    
    if len(request.GET.getlist('team')) == 0:
        team_filter = [0]
    for i in request.GET.getlist('team'):
        team_filter.append(int(i))
    
    # every team must fulfill all of the filter requirements 
    # to be passed to the stats view
    
    for team in teams:
        if ((team.division.id in division_filter) | (0 in division_filter)):
            if ((team.skillLevel.id in level_filter) | (0 in level_filter)):
                if ((team.club.id in club_filter) | (0 in club_filter)):
                    if ((team.id in team_filter) | (0 in team_filter)):
                        stats.append(team.get_stats())
    
    return render_to_response('core/stats/summary.html', {'user': request.user, 
                                                          'stats': stats,
                                                          'teams': teams,
                                                          'levels': levels,
                                                          'clubs': clubs,
                                                          'divisions': divisions,
                                                          'division_filter': division_filter,
                                                          'level_filter': level_filter,
                                                          'club_filter': club_filter,
                                                          'team_filter': team_filter,
                                                          'url': url,
                                                          'query_string': request.META['QUERY_STRING']})


def seeding(request):
    completedStatus = EventStatus.objects.get(name = "Completed")    
    seedingType = EventType.objects.get(name = "Seeding Game")
    currentSeason = Season.objects.get(isCurrentSeason = True)
    
    # completed events (seeding game type) (current season)
    events = Event.objects.filter(eventStatus = completedStatus, eventType = seedingType, season = currentSeason).order_by('-dateTimeEvent')
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
            
    return render_to_response('core/stats/seeding.html', {'user': request.user, 'events': eventList})

def season(request):
    completedStatus = EventStatus.objects.get(name = "Completed")    
    seasonType = EventType.objects.get(name = "Season Game")
    currentSeason = Season.objects.get(isCurrentSeason = True)
    
    # completed events (season game type) (current season)
    events = Event.objects.filter(eventStatus = completedStatus, eventType = seasonType, season = currentSeason).order_by('-dateTimeEvent')
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
            
    return render_to_response('core/stats/season.html', {'user': request.user, 'events': eventList})

@login_required
def playoffs(request):
    return render_to_response('core/stats/playoffs.html', {'user': request.user})

@login_required
def tournament(request):
    return render_to_response('core/stats/tournament.html', {'user': request.user})

@login_required
def record(request):
    confirmedStatus = EventStatus.objects.get(name = "Confirmed")
    completedStatus = EventStatus.objects.get(name = "Completed")
    team = request.user.get_profile().team
    currentSeason = Season.objects.get(isCurrentSeason = True)
    
    # calculate entry limit
    nowMinusEntryLimit = datetime.now() - timedelta(hours = int(Parameter.objects.get(name = 'stats.entry.limit').value))
    
    # confirmed events
    confirmedEvents = Event.objects.filter(eventStatus = confirmedStatus, homeTeam = team, season = currentSeason, dateTimeEvent__gt = nowMinusEntryLimit)
    confirmedEventsList = list()
    for object in confirmedEvents:
        homeGoals = EventGoal.objects.filter(event = object, team = object.homeTeam).count()
        awayGoals = EventGoal.objects.filter(event = object, team = object.awayTeam).count()
        confirmedEventsList.append({'id': object.id,
                               'homeTeam': object.homeTeam,
                               'awayTeam': object.awayTeam,
                               'eventType': object.eventType,
                               'dateTimeEvent': object.dateTimeEvent,
                               'rink': object.rink,
                               'eventStatus': object.eventStatus,
                               'score': "%s:%s" % (homeGoals, awayGoals)})

    # past due events
    pastdueEvents = Event.objects.filter(eventStatus = confirmedStatus, homeTeam = team, season = currentSeason, dateTimeEvent__lt = nowMinusEntryLimit)
    pastdueEventsList = list()
    for object in pastdueEvents:
        homeGoals = EventGoal.objects.filter(event = object, team = object.homeTeam).count()
        awayGoals = EventGoal.objects.filter(event = object, team = object.awayTeam).count()
        pastdueEventsList.append({'id': object.id,
                               'homeTeam': object.homeTeam,
                               'awayTeam': object.awayTeam,
                               'eventType': object.eventType,
                               'dateTimeEvent': object.dateTimeEvent,
                               'rink': object.rink,
                               'eventStatus': object.eventStatus,
                               'score': "%s:%s" % (homeGoals, awayGoals)})
    
    # completed events
    completedEvents = Event.objects.filter(eventStatus = completedStatus, homeTeam = team, season = currentSeason)
    completedEventsList = list()
    for object in completedEvents:
        canEdit = False
        if object.dateTimeEvent >= nowMinusEntryLimit:
            canEdit = True
            
        homeGoals = EventGoal.objects.filter(event = object, team = object.homeTeam).count()
        awayGoals = EventGoal.objects.filter(event = object, team = object.awayTeam).count()
        completedEventsList.append({'id': object.id,
                               'homeTeam': object.homeTeam,
                               'awayTeam': object.awayTeam,
                               'eventType': object.eventType,
                               'dateTimeEvent': object.dateTimeEvent,
                               'rink': object.rink,
                               'eventStatus': object.eventStatus,
                               'score': "%s:%s" % (homeGoals, awayGoals),
                               'canEdit': canEdit})
            
    return render_to_response('core/stats/record.html', {'user': request.user, 
                                                         'confirmedEvents': confirmedEventsList,
                                                         'pastdueEvents': pastdueEventsList,
                                                         'completedEvents': completedEventsList,
                                                         'hourLimit': Parameter.objects.get(name = 'stats.entry.limit'),
                                                         'currentSeason': Season.objects.get(isCurrentSeason = True)})

@login_required
def record_event(request, object_id):
    event = Event.objects.get(id = object_id)
    try:
        eventStats = EventStats.objects.get(event = event)
    except:
        eventStats = EventStats()    
        
    if request.method == 'GET':     
        teams = Team.objects.filter(Q(id = event.homeTeam.id) | Q(id = event.awayTeam.id))
        penaltyOffenses = PenaltyOffense.objects.all()
        goals = EventGoal.objects.filter(event = event).order_by('-id')
        penalties = EventPenalty.objects.filter(event = event).order_by('-id')
        suspensions = EventSuspension.objects.filter(event = event).order_by('-id')
        goalkeepersaves = EventGoalkeeperSaves.objects.filter(event = event).order_by('-id')
        
        return render_to_response('core/stats/event_record.html', 
                                                           {'user': request.user, 
                                                            'eventStats': eventStats,
                                                            'event': event, 
                                                            'teams': teams, 
                                                            'penaltyOffenses': penaltyOffenses,
                                                            'goals': goals,
                                                            'penalties': penalties,
                                                            'suspensions': suspensions,
                                                            'goalkeepersaves': goalkeepersaves})
    elif request.method == 'POST':
            
        event.eventStatus = EventStatus.objects.get(name = "Completed")
        event.save()
        
        eventStats.event = event

        if 'majorPenaltiesAssessed' in request.POST and not (request.POST['majorPenaltiesAssessed'] is None):
            eventStats.majorPenaltiesAssessed = True
        else:
            eventStats.majorPenaltiesAssessed = False
            
        eventStats.referee1Name = request.POST['referee1Name']
        eventStats.referee2Name = request.POST['referee2Name']
        eventStats.referee3Name = request.POST['referee3Name']
        eventStats.referee1Level = request.POST['referee1Level']
        eventStats.referee2Level = request.POST['referee2Level']
        eventStats.referee3Level = request.POST['referee3Level']
        eventStats.referee1IHOANum = request.POST['referee1IHOANum']
        eventStats.referee2IHOANum = request.POST['referee2IHOANum']
        eventStats.referee3IHOANum = request.POST['referee3IHOANum']
            
        goalsHome = EventGoal.objects.filter(Q(event = event) & Q(team = event.homeTeam)).count()
        goalsAway = EventGoal.objects.filter(Q(event = event) & Q(team = event.awayTeam)).count()
        
        if goalsHome > goalsAway:
            eventStats.winner = event.homeTeam
            eventStats.loser = event.awayTeam
        elif goalsHome < goalsAway:
            eventStats.winner = event.awayTeam
            eventStats.loser = event.homeTeam
        else:
            eventStats.tie = True
                        
        eventStats.save()
        
        return HttpResponseRedirect('/stats/event/%s' % event.id)
    
@login_required
def event(request, object_id):
    event = Event.objects.get(id = object_id)
    
    try:
        eventStats = EventStats.objects.get(event = event)
    except EventStats.DoesNotExist:
        return render_to_response('core/stats/event_detail.html', {'doesNotExist': True})
        
    teams = Team.objects.filter(Q(id = event.homeTeam.id) | Q(id = event.awayTeam.id))
    penaltyOffenses = PenaltyOffense.objects.all()
    goals = EventGoal.objects.filter(event = event).order_by('-id')
    penalties = EventPenalty.objects.filter(event = event).order_by('-id')
    suspensions = EventSuspension.objects.filter(event = event).order_by('-id')
    goalkeepersaves = EventGoalkeeperSaves.objects.filter(event = event).order_by('-id')
    
    homeGoals = EventGoal.objects.filter(event = event, team = event.homeTeam).count()
    awayGoals = EventGoal.objects.filter(event = event, team = event.awayTeam).count()
    
    return render_to_response('core/stats/event_detail.html', { 'doesNotExist': False,
                                                                'user': request.user, 
                                                                'eventStats': eventStats,
                                                                'event': event, 
                                                                'teams': teams, 
                                                                'penaltyOffenses': penaltyOffenses,
                                                                'goals': goals,
                                                                'penalties': penalties,
                                                                'suspensions': suspensions,
                                                                'goalkeepersaves': goalkeepersaves,
                                                                'homeGoals': homeGoals,
                                                                'awayGoals': awayGoals})

