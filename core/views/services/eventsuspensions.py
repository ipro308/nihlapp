from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, EventType, Rink, Season, EventStatus, EventSuspension, Team
from time import strptime, strftime
from datetime import datetime

@login_required
def detail(request):
    try:
        object = EventSuspension.objects.get(id = request.POST['object_id'])
        response = {'team': object.team.id, 
                    'player': object.player, 
                    'player_last_name': object.playerLastName}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')       
    
@login_required
def create(request): 

    try:
        event = Event.objects.get(id = request.POST['event_id'])
        team = Team.objects.get(id = request.POST['suspension_team'])

        object = EventSuspension()
        object.event = event
        object.team = team
        object.player = request.POST['suspension_player']
        object.playerLastName = request.POST['suspension_player_lastname']
        object.save()
        
        response = {'object_id': object.id,
                    'team': str(object.team), 
                    'player': object.player, 
                    'player_last_name': object.playerLastName}
        
    except Exception, error:
        response = {'error': str(error)}
    
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

@login_required
def delete(request): 
    try:
        object = EventSuspension(id = request.POST['object_id'])
        object.delete()
        response = {}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

        