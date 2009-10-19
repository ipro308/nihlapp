import os
from django.http import HttpResponse
from time import strftime

def pull(request):
       
    try:
        file = open("/home/vsemenov/logs/githook.log", 'a')
        file.write("%s: Git pull request via %s\n" % (strftime("%Y-%m-%d %H:%M:%S"), request.META['REQUEST_METHOD']))
        file.close()
        os.system("cd %s && touch dummy.pyc && find . -type f -name '*.pyc' | xargs rm && git pull" % (os.path.dirname(os.path.realpath(__file__))))
        os.system("touch /home/vsemenov/logs/nihlapp-restart")
        status = "success"
        
    except Exception, error:
        status = str(error)
        file = open("/home/vsemenov/logs/logs/githook.log", 'a')
        file.write("%s: Git pull request ERROR: %s\n" % (strftime("%Y-%m-%d %H:%M:%S"), status))
        file.close()
    
    return HttpResponse(status)
