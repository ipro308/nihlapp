from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Event, Season, EventStatus, Team, PenaltyOffense
from nihlapp.core.utils import TeamStats

@login_required
def summary(request):
    teams = TeamStats.objects.filter(season = Season.objects.get(isCurrentSeason = True))
    stats = list()
    for team in teams:
        stats.append(team.get_stats())
    
    return render_to_response('core/stats/summary.html', {'user': request.user, 'stats': stats})

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
def record_event(request, object_id):
    event = Event.objects.get(id = object_id)
    teams = Team.objects.filter(Q(id = event.homeTeam.id) | Q(id = event.awayTeam.id))
    penaltyOffenses = PenaltyOffense.objects.all()
    return render_to_response('core/stats/event.html', {'user': request.user, 'event': event, 'teams': teams, 'penaltyOffenses': penaltyOffenses})

    