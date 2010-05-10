from django.shortcuts import render_to_response

def help(request):
    return render_to_response('core/help/help.html', {'user': request.user})

def faq(request):
    return render_to_response('core/help/faq.html', {'user': request.user})

