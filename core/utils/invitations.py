from django.contrib.auth.models import Group
from nihlapp.core.models import Invitation, Club, Team
import hashlib

def generate_invitation(full_name, email, club, team, group = None):
    
    if group == None:
        try:
            # TODO: un-hardcode this to use a parameter
            group = Group.objects.get(name = "Team Admins")
        except: 
            raise Exception, "Unable to find default group."
         
    invitation = Invitation()
    invitation.name = full_name
    invitation.email = email
    invitation.club = club
    invitation.team = team
    invitation.used = False
    invitation.save()
    
    # generate unique hash
    hash = hashlib.sha256()
    # TODO: un-hardcode salt
    hash.update("invitation_%s_%s" % (invitation.id, "hockeypuck"))
    invitation.key = hash.hexdigest()
    invitation.save()
    
    return invitation.id

def mass_invite_team_admins():
    pass

def mass_invite_club_admins():
    pass

