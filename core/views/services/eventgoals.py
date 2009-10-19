from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, Team, EventGoal
from time import strptime, strftime
from datetime import datetime

@login_required
def create(request): 

    # attempt to save a goal
    try:
        event = Event.objects.get(id = request.POST['event_id'])
        teamFor = Team.objects.get(id = request.POST['goal_team'])
        
        # find out which team was scored against
        if event.homeTeam == teamFor:
            teamAgainst = event.awayTeam
        else:
            teamAgainst = event.homeTeam
            
        # populate goal object and call save
        goal = EventGoal()
        goal.event = event
        goal.time = datetime(*strptime("%s:%s" % (request.POST['goal_time_minute'], request.POST['goal_time_second']), "%M:%S")[:6])
        goal.team = teamFor
        goal.againstTeam = teamAgainst
        goal.period = request.POST['goal_period']
        goal.player = request.POST['goal_player']
        event.save()
        
        response = {'team': str(goal.team), 
                    'player': goal.player, 
                    'period': goal.period,
                    'time_minute': strftime("%M", goal.time.timetuple()),
                    'time_second': strftime("%S", goal.time.timetuple())}
        
    except Exception, error:
        response = {'error': str(error)}
    
    #response = {'error': "got this: %s!" % (request.POST['event_am'])}
    
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    
