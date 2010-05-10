# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseRedirect
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
            
            newuser.set_password(form.cleaned_data['password'])
            
            newuser.save()

            newuser.groups.add(form.cleaned_data['group'])
            newuser.save()

            newprofile = UserProfile()
            newprofile.email = form.cleaned_data['email']
            newprofile.club = form.cleaned_data['club']
            newprofile.team = form.cleaned_data['team']
            newprofile.phone = form.cleaned_data['phone']
            newprofile.user = newuser
            newprofile.save()
            return HttpResponseRedirect('/accounts/detail/%d' % newuser.id)
    else:
        form = CreateUserForm() # An unbound form

    return render_to_response('core/user_form.html', {
        'form': form, 'user': request.user
    })

@login_required
def create_team_user(request,team_id):
    if request.method == 'POST': # If the form has been submitted...
        form = CreateUserForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            newuser = User()
            newuser.username = form.cleaned_data['username']

            newuser.first_name = form.cleaned_data['firstName']
            newuser.last_name = form.cleaned_data['lastName']
            newuser.email = form.cleaned_data['email']

            newuser.set_password(form.cleaned_data['password'])

            newuser.save()

            newuser.groups.add(form.cleaned_data['group'])
            newuser.save()

            newprofile = UserProfile()
            newprofile.email = form.cleaned_data['email']
            newprofile.club = form.cleaned_data['club']
   #         newprofile.team = request.team_id
            newprofile.phone = form.cleaned_data['phone']
            newprofile.user = newuser
            newprofile.save()
            return HttpResponseRedirect('/accounts/detail/%d' % newuser.id)
    else:
        form = CreateUserForm() # An unbound form

    return render_to_response('core/user_form.html', {
        'form': form, 'user': request.user
    })

@login_required
def update(request, object_id):
    
    # load initial data for the form
    user = User.objects.get(id = object_id)
    data = {'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'password': 'keepexistinguserpassword',
            'password_confirm': 'keepexistinguserpassword',
            'is_active': user.is_active,
            'group': user.groups.all()[0].id,
            'team': user.get_profile().team.id,
            'club': user.get_profile().club.id,
            'phone': user.get_profile().phone}
    
    if request.method == 'POST': 
        form = CreateUserForm(request.POST, initial = data) 
        if form.is_valid():
            newuser = User.objects.get(id = object_id)
            newuser.username = form.cleaned_data['username']

            newuser.first_name = form.cleaned_data['firstName'] 
            newuser.last_name = form.cleaned_data['lastName']
            newuser.email = form.cleaned_data['email']
            
            if form.cleaned_data['password'] != 'keepexistinguserpassword':
                newuser.set_password(form.cleaned_data['password'])

            newuser.groups.clear()
            newuser.groups.add(form.cleaned_data['group'])

            newuser.save()

            newprofile = newuser.get_profile()
            newprofile.email = form.cleaned_data['email']
            newprofile.club = form.cleaned_data['club']
            newprofile.team = form.cleaned_data['team']
            newprofile.phone = form.cleaned_data['phone']
            newprofile.user = newuser
            newprofile.save()
            return HttpResponseRedirect('/accounts/detail/%d' % newprofile.id)
    else:
        form = CreateUserForm(initial = data)

    return render_to_response('core/user_form.html', {
        'form': form, 'user': request.user, 'object': data
    })

def confirm(request, object_id):
	return render_to_response('core/account/confirm.html', {'object_id': object_id})

def logout(request):
	response = logout(request, next_page='/accounts/logout/')
	return response
	# Redirect to a success page.