# -*- coding: utf-8 -*-
from django.template import loader, Context
from django.core.mail import send_mail
from django.db.models import Q
from nihlapp.core.models import Invitation, Parameter, UserProfile, Event
from django.shortcuts import render_to_response

# 
# Invitation into NIHL system.
#

def new_send_invitation(request,invite_id):
	if request.method == 'POST':
		message = request.POST['message'];
		
		try:
			invitation = Invitation.objects.get(id = invite_id)
		except:
				raise Exception, "Unable to find invitation id: %s." % invitation_id
		try:
			send_mail('%s Please register with NIHL' % Parameter.objects.get(name = "email.prefix"),
				message,
				"%s <%s>" % (Parameter.objects.get(name = "email.from"), Parameter.objects.get(name = "email.noreply")),
				[invitation.email],
				fail_silently=False)
				
		except Exception, error:
			raise Exception, "Unable to send invitation: %s." % error
		
		return render_to_response('core/invitations/confirm_send.html', {'name': invitation.name,
										'email': invitation.email,
										})
	else:
		raise Exception, "Unable to send invitation: %s." % error

def send_invitation(invitation_id):
    
    try:
        invitation = Invitation.objects.get(id = invitation_id)
    except:
        raise Exception, "Unable to find invitation id: %s." % invitation_id
        
    try:
        template = loader.get_template('email/invitation.html')
        context = Context({
                           'siteHostname': Parameter.objects.get(name = "site.hostname"),
                           'invitation': invitation
                           })
        send_mail('%s Please register with NIHL' % Parameter.objects.get(name = "email.prefix"), 
                  template.render(context), 
                  "%s <%s>" % (Parameter.objects.get(name = "email.from"), Parameter.objects.get(name = "email.noreply")), 
                  [invitation.email], 
                  fail_silently=False)
    except Exception, error:
        raise Exception, "Unable to send invitation: %s." % error

#
# Email confirmation after user created email account.
#
def send_confirmation(userProfile_id):
    
    try:
        userProfile = UserProfile.objects.get(id = userProfile_id)
    except:
        raise Exception, "Unable to find confirmation id: %s." % userProfile_id
        
    try:
        template = loader.get_template('email/confirmation.html')
        context = Context({
                           'siteHostname': Parameter.objects.get(name = "site.hostname"),
                           'confirmation': userProfile.confirmation,
                           'userName': userProfile.user.get_full_name()
                           })
        send_mail('%s Please confirm your email address' % Parameter.objects.get(name = "email.prefix"), 
                  template.render(context), 
                  "%s <%s>" % (Parameter.objects.get(name = "email.from"), Parameter.objects.get(name = "email.noreply")), 
                  [userProfile.email], 
                  fail_silently=False)
    except Exception, error:
        raise Exception, "Unable to send confirmation: %s." % error    
    
#
# Notifies home team managers of scheduling request from away team.
#
def send_event_scheduled_notification(event_id):
    try:
        event = Event.objects.get(id = event_id)
    except:
        raise Exception, "Unable to find event id: %s." % event_id
        
    try:
        # get managers of homeTeam
        managers = UserProfile.objects.filter(team = event.homeTeam)
    except:
        raise Exception, "Unable to locate team's managers."
        
    try:
        for manager in managers:
            template = loader.get_template('email/event_scheduled.html')
            context = Context({
                               'siteHostname': Parameter.objects.get(name = "site.hostname"),
                               'event': event,
                               'manager': manager
                               })
            send_mail('%s Game scheduling request from %s' % (Parameter.objects.get(name = "email.prefix"), event.awayTeam), 
                      template.render(context), 
                      "%s <%s>" % (Parameter.objects.get(name = "email.from"), Parameter.objects.get(name = "email.noreply")), 
                      [manager.email], 
                      fail_silently = False)
    except Exception, error:
        raise Exception, "Unable to send notification: %s." % error

#
# Notifies away team managers about scheduling confirmation from home team.
#
def send_event_confirmed_notification(event_id):
    try:
        event = Event.objects.get(id = event_id)
    except:
        raise Exception, "Unable to find event id: %s." % event_id
        
    try:
        # get managers of awayTeam
        managers = UserProfile.objects.filter(team = event.awayTeam)
    except:
        raise Exception, "Unable to locate team's managers."
        
    try:
        for manager in managers:
            template = loader.get_template('email/event_confirmed.html')
            context = Context({
                               'siteHostname': Parameter.objects.get(name = "site.hostname"),
                               'event': event,
                               'manager': manager
                               })
            send_mail('%s Game confirmed by %s' % (Parameter.objects.get(name = "email.prefix"), event.homeTeam), 
                      template.render(context), 
                      "%s <%s>" % (Parameter.objects.get(name = "email.from"), Parameter.objects.get(name = "email.noreply")), 
                      [manager.email], 
                      fail_silently = False)
    except Exception, error:
        raise Exception, "Unable to send notification: %s." % error

#
# Notifies away team managers about scheduling rejection from home team.
#
def send_event_rejected_notification(event_id):
    try:
        event = Event.objects.get(id = event_id)
    except:
        raise Exception, "Unable to find event id: %s." % event_id
        
    try:
        # get managers of awayTeam
        managers = UserProfile.objects.filter(team = event.awayTeam)
    except:
        raise Exception, "Unable to locate team's managers."
        
    try:
        for manager in managers:
            template = loader.get_template('email/event_rejected.html')
            context = Context({
                               'siteHostname': Parameter.objects.get(name = "site.hostname"),
                               'event': event,
                               'manager': manager
                               })
            send_mail('%s Game requested rejected by %s' % (Parameter.objects.get(name = "email.prefix"), event.homeTeam), 
                      template.render(context), 
                      "%s <%s>" % (Parameter.objects.get(name = "email.from"), Parameter.objects.get(name = "email.noreply")), 
                      [manager.email], 
                      fail_silently = False)
    except Exception, error:
        raise Exception, "Unable to send notification: %s." % error

#
# Notifies home team and away team managers about stats entry for event.
#
def send_event_completed_notifications(event_id):
    try:
        event = Event.objects.get(id = event_id)
    except:
        raise Exception, "Unable to find event id: %s." % event_id
        
    try:
        # get managers of both teams
        managers = UserProfile.objects.filter(Q(team = event.awayTeam) | Q(team = event.homeTeam))
    except:
        raise Exception, "Unable to locate teams' managers."
        
    try:
        for manager in managers:
            template = loader.get_template('email/event_stats_entered.html')
            context = Context({
                               'siteHostname': Parameter.objects.get(name = "site.hostname"),
                               'event': event,
                               'manager': manager
                               })
            send_mail('%s Game statistics entered for %s v. %s' % (Parameter.objects.get(name = "email.prefix"), event.homeTeam, event.awayTeam), 
                      template.render(context), 
                      "%s <%s>" % (Parameter.objects.get(name = "email.from"), Parameter.objects.get(name = "email.noreply")), 
                      [manager.email], 
                      fail_silently = False)
    except Exception, error:
        raise Exception, "Unable to send notification: %s." % error    

def send_seeding_start_notification():
    pass

def send_season_start_notification():
    pass

