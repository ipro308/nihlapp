from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Event, Season, EventStatus, Team, PenaltyOffense, EventGoal, EventPenalty, EventSuspension, EventGoalkeeperSaves
from nihlapp.core.utils import TeamStats
from django.db.models import Q


def summary(request):
    teams = TeamStats.objects.filter(season = Season.objects.get(isCurrentSeason = True))
    stats = list()
    for team in teams:
        stats.append(team.get_stats())
    
    return render_to_response('core/stats/summary.html', {'user': request.user, 'stats': stats})


def seeding(request):
    return render_to_response('core/stats/seeding.html', {'user': request.user})


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
def record_event(request, object_id):
    event = Event.objects.get(id = object_id)
    
    if request.method == 'GET':
        teams = Team.objects.filter(Q(id = event.homeTeam.id) | Q(id = event.awayTeam.id))
        penaltyOffenses = PenaltyOffense.objects.all()
        goals = EventGoal.objects.filter(event = event).order_by('-id')
        penalties = EventPenalty.objects.filter(event = event).order_by('-id')
        suspensions = EventSuspension.objects.filter(event = event).order_by('-id')
        goalkeepersaves = EventGoalkeeperSaves.objects.filter(event = event).order_by('-id')
        
        return render_to_response('core/stats/event.html', {'user': request.user, 
                                                            'event': event, 
                                                            'teams': teams, 
                                                            'penaltyOffenses': penaltyOffenses,
                                                            'goals': goals,
                                                            'penalties': penalties,
                                                            'suspensions': suspensions,
                                                            'goalkeepersaves': goalkeepersaves})
    elif request.method == 'POST':
        eventStats = EventStats()
        eventStats.event = event

        if request.POST['majorPenaltiesAssessed'] == 'on':
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

    
    
    