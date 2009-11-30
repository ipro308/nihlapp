from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from nihlapp.core.models import Event, EventType, Rink, Season, EventStatus, Matchup
from time import strptime, strftime
from datetime import datetime

@login_required
def schedule(request):
    try:
        event = Event()
        matchup = Matchup()
        availableStatus = EventStatus.objects.get(name = "Available")
        scheduledStatus = EventStatus.objects.get(name = "Scheduled")
        
        try:
            event = Event.objects.get(id = request.POST['event_id'])
            matchup = Matchup.objects.get(id = request.POST['matchup_id'])
        except:
            raise Exception, "Unable to find specified time slot."
        
        # check to see if event has already progressed into scheduling, in that case we can not delete it
        if event.eventStatus != availableStatus:
            raise Exception, "Game has already been scheduled for this time slot."

        event.eventStatus = scheduledStatus
        event.awayTeam = request.user.get_profile().team
        event.matchup = matchup
        event.save()
        
        # generate email response
        send_event_scheduled_notification(event.id)
        
        response = {'status': "Game requested on <b>%s</b> at <a href='%s'>%s</a>." % (event, 
                                                                                       event.rink.get_absolute_url(), 
                                                                                       event.rink)}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    


@login_required
def confirm(request):
    try:
        event = Event()
        scheduledStatus = EventStatus.objects.get(name = "Scheduled")
        confirmedStatus = EventStatus.objects.get(name = "Confirmed")
        
        try:
            event = Event.objects.get(id = request.POST['event_id'])
            #matchup = Matchup.objects.get(id = request.POST['matchup_id'])
        except:
            raise Exception, "Unable to find specified time slot."
        
        # check to see if event has already progressed into scheduling, in that case we can not delete it
        if event.eventStatus != scheduledStatus:
            raise Exception, "Game (id: %d) has not been scheduled." % event.id

        event.eventStatus = confirmedStatus
        event.save()
        
        # generate email response
        send_event_confirmed_notification(event.id)
        
        response = {'status': "Confirmed for <b>%s</b> at <a href='%s'>%s</a>." % (event, 
                                                           event.rink.get_absolute_url(), 
                                                           event.rink)}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    


@login_required
def reject(request):
    try:
        event = Event()
        availableStatus = EventStatus.objects.get(name = "Available")
        scheduledStatus = EventStatus.objects.get(name = "Scheduled")
        
        try:
            event = Event.objects.get(id = request.POST['event_id'])
            #matchup = Matchup.objects.get(id = request.POST['matchup_id'])
        except:
            raise Exception, "Unable to find specified time slot."
        
        # check to see if event has already progressed into scheduling, in that case we can not delete it
        if event.eventStatus != scheduledStatus:
            raise Exception, "Game (id: %d) has not been scheduled." % event.id

        event.eventStatus = availableStatus
        event.awayTeam = None
        event.matchup = None
        event.save()
        
        # generate email response
        send_event_rejected_notification(event.id)
        
        response = {'status': "Rejected game request."}
    except Exception, error:
        response = {'error': str(error)}
        
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype = 'application/json')    


