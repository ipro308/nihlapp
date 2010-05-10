from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, EventType, Rink, Season, EventStatus, EventPenalty, PenaltyOffense, Team
from time import strptime, strftime
from datetime import datetime

@login_required
def detail(request):
    try:
        object = EventPenalty.objects.get(id = request.POST['object_id'])
        response = {'object_id': object.id,
                    'team': object.team.id, 
                    'player': object.player, 
                    'offense': object.penaltyOffense.id, 
                    'period': object.period,
                    'time_minute': strftime("%M", object.penaltyTime.timetuple()),
                    'time_second': strftime("%S", object.penaltyTime.timetuple()),
                    'time_on_minute': strftime("%M", object.timeOn.timetuple()),
                    'time_on_second': strftime("%S", object.timeOn.timetuple()),
                    'time_off_minute': strftime("%M", object.timeOff.timetuple()),
                    'time_off_second': strftime("%S", object.timeOff.timetuple())}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')       
    
@login_required
def create(request): 

    try:
        event = Event.objects.get(id = request.POST['event_id'])
        team = Team.objects.get(id = request.POST['penalty_team'])
        offense = PenaltyOffense.objects.get(id = request.POST['penalty_offense'])
        
        object = EventPenalty()
        object.event = event
        object.team = team
        object.period = request.POST['penalty_period']
        object.player = request.POST['penalty_player']
        object.penaltyOffense = offense
        object.penaltyTime = datetime(*strptime("01/01/2001 01:%s:%s" % (request.POST['penalty_time_minute'], 
                                                                         request.POST['penalty_time_second']), 
                                                                         "%m/%d/%Y %I:%M:%S")[:6])
        object.timeOn = datetime(*strptime("01/01/2001 01:%s:%s" % (request.POST['penalty_time_on_minute'], 
                                                                    request.POST['penalty_time_on_second']), 
                                                                    "%m/%d/%Y %I:%M:%S")[:6])
        object.timeOff = datetime(*strptime("01/01/2001 01:%s:%s" % (request.POST['penalty_time_off_minute'], 
                                                                     request.POST['penalty_time_off_second']), 
                                                                     "%m/%d/%Y %I:%M:%S")[:6])        
        object.save()
        
        response = {'object_id': object.id,
                    'team': str(object.team), 
                    'player': object.player, 
                    'offense': str(object.penaltyOffense), 
                    'period': object.period,
                    'time_minute': strftime("%M", object.penaltyTime.timetuple()),
                    'time_second': strftime("%S", object.penaltyTime.timetuple()),
                    'time_on_minute': strftime("%M", object.timeOn.timetuple()),
                    'time_on_second': strftime("%S", object.timeOn.timetuple()),
                    'time_off_minute': strftime("%M", object.timeOff.timetuple()),
                    'time_off_second': strftime("%S", object.timeOff.timetuple())}
        
    except Exception, error:
        response = {'error': str(error)}
    
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

@login_required
def delete(request): 
    try:
        object = EventPenalty(id = request.POST['object_id'])
        object.delete()
        response = {}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

