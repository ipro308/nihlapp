from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, EventType, Rink, Season, EventStatus
from time import strptime, strftime
from datetime import datetime

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
        eventType = event.eventType
        rink = event.rink
        date = event.dateTimeEvent
        
        response = {'eventType': eventType.name, 'rink': rink.name, 'date': strftime("%m/%d/%Y %I:%M %p", date.timetuple())}
        
    except Exception, error:
        response = {'error': str(error)}
    
    #response = {'error': "got this: %s!" % (request.POST['event_am'])}
    
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    
