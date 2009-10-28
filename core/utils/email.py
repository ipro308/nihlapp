from django.template import loader, Context
from django.core.mail import send_mail
from nihlapp.core.models import Invitation, Parameter

def send_invitation(invitation_id):
    
    try:
        invitation = Invitation.objects.get(id = invitation_id)
    except:
        raise Exception, "Unable to find invitation id: %s." % invitation_id
        
    try:
        template = loader.get_template('email/invitation.html')
        context = Context({
                           'siteHostname': new_data['first_name'],
                           'invitation': invitation
                           })
        send_mail('%s Please register with NIHL' % Parameter.objects.get(name = "email.prefix"), 
                  template.render(context), 
                  "%s <%s>" % (Parameter.objects.get(name = "email.from"), Parameter.objects.get(name = "email.noreply")), 
                  [invitation.email], 
                  fail_silently=False)
    except error:
        raise Exception, "Unable to send invitation: %s." % error
    
def send_event_scheduled_notification():
    pass

def send_event_confirmed_notification():
    pass

def send_event_cancelled_notification():
    pass

def send_seeding_start_notification():
    pass

def send_season_start_notification():
    pass

