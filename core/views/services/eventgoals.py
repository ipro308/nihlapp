from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, Team, EventGoal
from time import strptime, strftime
from datetime import datetime

@login_required
def detail(request):
    try:
        object = EventGoal.objects.get(id = request.POST['object_id'])
        response = {'team': object.team.id, 
                    'player': object.player, 
                    'period': object.period,
                    'time_minute': strftime("%M", object.time.timetuple()),
                    'time_second': strftime("%S", object.time.timetuple())}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')       
    
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
        object = EventGoal()
        object.event = event
        object.time = datetime(*strptime("01/01/2001 01:%s:%s" % (request.POST['goal_time_minute'], 
                                                                  request.POST['goal_time_second']), 
                                                                  "%m/%d/%Y %I:%M:%S")[:6])
        object.team = teamFor
        object.againstTeam = teamAgainst
        object.period = request.POST['goal_period']
        object.player = request.POST['goal_player']
        object.save()
        
        response = {'object_id': object.id,
                    'team': str(object.team), 
                    'player': object.player, 
                    'period': object.period,
                    'time_minute': strftime("%M", object.time.timetuple()),
                    'time_second': strftime("%S", object.time.timetuple())}
        
    except Exception, error:
        response = {'error': str(error)}
    
    #response = {'error': "got this: %s!" % (request.POST['event_am'])}
    
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

@login_required
def delete(request): 
    try:
        object = EventGoal(id = request.POST['object_id'])
        object.delete()
        response = {}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

        