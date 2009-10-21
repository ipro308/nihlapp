from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, EventType, Rink, Season, EventStatus
from time import strptime, strftime
from datetime import datetime

@login_required
def detail(request):
    try:
        object = Event.objects.get(id = request.POST['object_id'])
        response = {'type': object.eventType.id, 
                    'rink': object.rink.id, 
                    'date': strftime("%m/%d/%Y", object.dateTimeEvent.timetuple()),
                    'hour': strftime("%I", object.dateTimeEvent.timetuple()),
                    'minute': strftime("%M", object.dateTimeEvent.timetuple()),
                    'am': strftime("%p", object.dateTimeEvent.timetuple())}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')       
    
@login_required
def create(request):
    
    # attempt to create a new event
    try:
        event = Event()
        event.dateTimeEvent = datetime(*strptime("%s %s:%s %s" % (request.POST['event_date'], 
                                                        request.POST['event_hour'], 
                                                        request.POST['event_minute'], 
                                                        request.POST['event_am']), "%m/%d/%Y %I:%M %p")[:6])
        event.eventStatus = EventStatus.objects.get(name = "Available")
        event.eventType = EventType.objects.get(id = request.POST['event_type'])
        event.rink = Rink.objects.get(id = request.POST['event_rink'])
        event.homeTeam = request.user.get_profile().team
        event.season = Season.objects.get(isCurrentSeason = True)
        event.save()
        
        #timeSlots = Event.objects.all().filter(eventType = request.POST['event_type'], homeTeam = request.user.get_profile().team, season = Season.objects.get(isCurrentSeason = True)).count()
        #timeSlot = timeSlots + 1
        
        response = {'object_id': event.id,
                    'eventType': str(event.eventType), 
                    'rink': str(event.rink), 
                    'date': strftime("%b %e, %Y", event.dateTimeEvent.timetuple()),
                    'time': strftime("%I:%M %p", event.dateTimeEvent.timetuple())}
        
    except Exception, error:
        response = {'error': str(error)}
    
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

@login_required
def delete(request): 
    try:
        object = Event.objects.get(id = request.POST['object_id'])
        availableStatus = EventStatus.objects.get(name = "Available")
        
        # check to see if event has already progressed into scheduling, in that case we can not delete it
        if object.eventStatus != availableStatus:
            raise Exception, "Game has already been scheduled for this time slot."

        object.delete()
        response = {}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    

