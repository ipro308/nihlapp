from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Invitation, InvitationForm, Team, Club, UserProfile
from django.db.models import Q
from nihlapp.core.utils.invitations import generate_invitation
from nihlapp.core.utils.email import send_invitation, send_confirmation
from django.contrib.auth.models import User, Group
#from datetime import datetime, timedelta

def invitation(request, key):
    
    if request.method == 'GET':
        try:
            invitation = Invitation.objects.get(key = key)
            invitationFound = True
            form = InvitationForm()
        except Exception, error:
            invitation = None
            invitationFound = False
            form = None
            
        return render_to_response('core/invitations/invite.html', {'invitation': invitation, 
                                                                   'invitationFound': invitationFound,
                                                                   'form': form,
                                                                   'key': key})            
    else:
        form = ContactForm(request.POST)
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
            
            return HttpResponseRedirect('/invitation/done/%s' %(invitation.email))
        
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


def invitation_done(request):
    return render_to_response('core/invitations/invite_done.html')

def confirm_email(reqest):
    
    try:
        confirmation = UserProfile.objects.get(confirmation = key)
        confirmationFound = True
    except Exception, error:
        confirmation = None
        confirmationFound = False 
    
    return render_to_response('core/invitations/confirm_email.html', {'confirmation': confirmation, 
                                                                      'confirmationFound': confirmationFound})

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
    
