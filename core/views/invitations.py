from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Invitation, InvitationForm, Team, Club
from django.db.models import Q
from nihlapp.core.utils.invitations import generate_invitation
from nihlapp.core.utils.email import send_invitation
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
            # create account
            return HttpResponseRedirect('/core/invitations/done')
        
    

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