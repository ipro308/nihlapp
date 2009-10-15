import os
from django.http import HttpResponse

def pull(request):
   
    try:
        os.system("cd %s && cd ../../ && touch dummy.pyc && find . -type f -name '*.pyc' | xargs rm && git pull && ../apache2/bin/restart" % (os.path.dirname(os.path.realpath(__file__))))
        status = "success"
    except Exception, error:
        status = str(error)
    
    return HttpResponse(status)
