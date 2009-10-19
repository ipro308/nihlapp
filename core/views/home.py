from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from nihlapp.core.models import Team, Season, Event, EventStatus

def summary(request):
    completed = EventStatus.objects.get(name = 'Completed')
    currentSeason = Season.objects.get(isCurrentSeason = True)
    numTeams = Team.objects.filter(season = currentSeason).count()
    numGames = Event.objects.filter(Q(season = currentSeason) & Q(eventStatus = completed)).count()
    return render_to_response('core/home/summary.html', {'user': request.user, 
                                                         'currentSeason': currentSeason,
                                                         'numTeams': numTeams,
                                                         'numGames': numGames})

def deadlines(request):
    return render_to_response('core/home/deadlines.html', {'user': request.user})

def teams(request):
    teams = Team.objects.order_by('name')
    return render_to_response('core/home/teams.html', {'user': request.user, 'teams': teams})
