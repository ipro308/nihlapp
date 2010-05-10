from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, EventType, Rink, Season, EventStatus, EventGoalkeeperSaves, Team

@login_required
def detail(request):
    try:
        object = EventGoalkeeperSaves.objects.get(id = request.POST['object_id'])
        response = {'team': object.team.id, 
                    'player': object.player, 
                    'first': object.firstPeriodSaves,
                    'second': object.secondPeriodSaves,
                    'third': object.thirdPeriodSaves,
                    'ot': object.overtimeSaves}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')       
    
@login_required
def create(request): 

    # attempt to save a goal
    try:
        event = Event.objects.get(id = request.POST['event_id'])
        teamFor = Team.objects.get(id = request.POST['saves_team'])
        
        # find out which team was scored against
        if event.homeTeam == teamFor:
            teamAgainst = event.awayTeam
        else:
            teamAgainst = event.homeTeam
            
        # populate goalkeeper object and call save
        object = EventGoalkeeperSaves()
        object.event = event
        object.team = teamFor
        object.againstTeam = teamAgainst
        object.player = request.POST['saves_player']
        object.firstPeriodSaves = request.POST['saves_1st']
        object.secondPeriodSaves = request.POST['saves_2nd']
        object.thirdPeriodSaves = request.POST['saves_3rd']
        object.overtimeSaves = request.POST['saves_ot']
        object.save()
        
        response = {'object_id': object.id,
                    'team': str(object.team), 
                    'player': object.player, 
                    'first': object.firstPeriodSaves,
                    'second': object.secondPeriodSaves,
                    'third': object.thirdPeriodSaves,
                    'ot': object.overtimeSaves}
        
    except Exception, error:
        response = {'error': str(error)}
    
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

@login_required
def delete(request): 
    try:
        object = EventGoalkeeperSaves(id = request.POST['object_id'])
        object.delete()
        response = {}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

