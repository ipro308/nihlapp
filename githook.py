import os
from django.http import HttpResponse

def pull(request):
   
    try:
        file = open("/home/vsemenov/githook.log", 'a')
        file.write("Git pull request via %s\n" % (request.META['REQUEST_METHOD']))
        file.close()

        os.system("cd %s && touch dummy.pyc && find . -type f -name '*.pyc' | xargs rm && git pull" % (os.path.dirname(os.path.realpath(__file__))))
        status = "success"
    except Exception, error:
        status = str(error)
        file = open("/home/vsemenov/githook.log", 'a')
        file.write("Git pull request ERROR: %s\n" % (status))
        file.close()
    
    return HttpResponse(status)
