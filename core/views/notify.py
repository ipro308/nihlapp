from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from nihlapp.core.models import User, Parameter

@login_required
def index(request):
    
    return render_to_response('core/notify/index.html', {'user': request.user, 
                                                         'users': User.objects.all(), 
                                                         'emailPrefix': Parameter.objects.get(name = "email.prefix")})

@login_required
def send(request):
    
    errorMessage = False
    
    try:
        send_mail("%s %s" % (Parameter.objects.get(name = "email.prefix"), request.POST['subject']), 
                  request.POST['message'], 
                  Parameter.objects.get(name = "email.from"),
                  [User.objects.get(id = request.POST['to']).get_profile().email], 
                  fail_siletnly = False)
    except Exception, error:
        errorMessage = str(error)   
        
    return render_to_response('core/notify/send.html', {'user': request.user, 'error': errorMessage})
