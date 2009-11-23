from django.http import Http404
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import User, UserProfile, CreateUserForm, Team, Club
from django.shortcuts import render_to_response

@login_required
def create(request):
    if request.method == 'POST': # If the form has been submitted...
		form = CreateUserForm(request.POST) # A form bound to the POST data
		if form.is_valid():
		    newuser = User()
         	newuser.username = form.cleaned_data['username']
         	
         	newuser.first_name = form.cleaned_data['firstName'] 
         	newuser.last_name = form.cleaned_data['lastName']
         	newuser.email = form.cleaned_data['email']
         	newuser.password = form.cleaned_data['password']
         	#newuser.groups.add(form.cleaned_data['group'])
         	
         	newuser.save()
         	
         	newprofile = UserProfile()
         	newprofile.email = form.cleaned_data['email']
         	newprofile.club = form.cleaned_data['club']
         	newprofile.team = form.cleaned_data['team']
         	newprofile.phone = form.cleaned_data['phone']
         	newprofile.user = newuser
         	newprofile.save()
#            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
    	form = CreateUserForm() # An unbound form

    return render_to_response('core/user_form.html', {
        'form': form, 'user': request.user
    })

