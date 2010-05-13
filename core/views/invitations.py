# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Invitation, InvitationForm, Team, Club, UserProfile
from django.db.models import Q
from nihlapp.core.utils.invitations import generate_invitation
from nihlapp.core.utils.email import send_invitation, send_confirmation
from django.contrib.auth.models import User, Group
from nihlapp.core.models.userProfile import SendInviteForm
from django.template import loader, Context
from nihlapp.core.models import Parameter
import hashlib

def invitation(request, key):
    
    try:
        invitation = Invitation.objects.get(key = key)
        invitationFound = True
        form = InvitationForm()
    except Exception, error:
        invitation = None
        invitationFound = False
        form = None
    
    if request.method == 'GET':
        pass
    
    else:
        form = InvitationForm(request.POST)
        if form.is_valid():
            
            # create user account for invitee
            user = User()
            invitation = Invitation.objects.get(key = key)
            user.username = form.cleaned_data['username']
            name = invitation.name.split(' ')
            user.first_name = name[0]
            user.last_name = name[1]
            user.email = invitation.email
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            user.groups.add(invitation.group)
            user.save()
            
            userProfile = UserProfile()
            userProfile.user = user
            userProfile.team = invitation.team
            userProfile.club = invitation.club
            userProfile.email = invitation.email
            userProfile.save()
            
            # mark invitation as used
            invitation.used = True
            invitation.save()
            
            # generate confirmation email
            hash = hashlib.sha256()
            # TODO: un-hardcode salt
            hash.update("confirmation_%s_%s" % (userProfile.id, "hockeypuck"))
            userProfile.confirmation = hash.hexdigest()
            userProfile.confirmed = False
            userProfile.save()
            
            send_confirmation(userProfile.id)
            
            return HttpResponseRedirect('/invitation/done/%s' % (userProfile.id))
        
    return render_to_response('core/invitations/invite.html', {'invitation': invitation, 
                                                               'invitationFound': invitationFound,
                                                               'form': form,
                                                               'key': key})         
        
"""
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    team = models.ForeignKey(Team, verbose_name = "User's Team")
    club = models.ForeignKey(Club, verbose_name = "User's Club")
    email = models.EmailField("Email", max_length = 50)
    phone = models.CharField("Phone", max_length = 10)

class Invitation(models.Model):
    key = models.CharField("Invitation Key", max_length = 64, unique = True)
    name = models.CharField("Full Name", max_length = 30)
    email = models.EmailField("Email")
    group = models.ForeignKey(Group, verbose_name = "Default Group")
    team = models.ForeignKey(Team, verbose_name = "Team")
    club = models.ForeignKey(Club, verbose_name = "Club")
    used = models.BooleanField("Used", default = False)
"""


def invitation_done(request, user_profile_id):
    
    try:
        userProfile = UserProfile.objects.get(id = user_profile_id)
    except:
        raise Exception, "Unable to find confirmation id: %s." % user_profile_id
    
    return render_to_response('core/invitations/invitation_done.html', {'email': userProfile.email})

def confirm_email(reqest, key):
    
    try:
        confirmation = UserProfile.objects.get(confirmation = key)
        confirmationFound = True
        # activate user's account
        confirmation.user.is_active = True
        confirmation.user.save()
        # set email confirmed flag in user profile
        confirmation.confirmed = True
        confirmation.save()
    except Exception, error:
        key = str()
        confirmation = None
        confirmationFound = False 
    
    return render_to_response('core/invitations/confirm_email.html', {'confirmation': confirmation, 
                                                                      'confirmationFound': confirmationFound,
                                                                      'key': key})

@login_required
def generate(request):
    
    # TODO: error handling
    
    invitation_id = generate_invitation(request.GET['name'], 
                                        request.GET['email'], 
                                        Club.objects.get(id = request.GET['club_id']), 
                                        Team.objects.get(id = request.GET['team_id']))
    send_invitation(invitation_id)
    
    invitation = Invitation.objects.get(id = invitation_id)
    
    return render_to_response('core/invitations/generate.html', {'name': invitation.name, 
                                                                 'email': invitation.email})
    
@login_required
def edit_invite(request):
	
	invitation_id = generate_invitation(request.GET['name'],
					request.GET['email'],
					Club.objects.get(id = request.GET['club_id']),
					Team.objects.get(id = request.GET['team_id']))
	
	try:
		invitation = Invitation.objects.get(id = invitation_id)
	except:
		raise Exception, "Unable to find invitation id: %s." % invitation_id
	
	template = loader.get_template('email/invitation.html')
	context = Context({'siteHostname': Parameter.objects.get(name = "site.hostname"), 'invitation': invitation})
	message = template.render(context)
	name = request.GET['name']
	email =request.GET['email']
	data = {'name':name,'email':email,'message':message}
	print data
	invitation_form = SendInviteForm(data)
	invitation_id = generate_invitation(
			request.GET['name'],
			request.GET['email'],
			Club.objects.get(id = request.GET['club_id']),
			Team.objects.get(id = request.GET['team_id']))
	return render_to_response('core/invitations/generate.html', {'name': name, 'email': email, 'form' : invitation_form, 'invitation_id':invitation_id})

	