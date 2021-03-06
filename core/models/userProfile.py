# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from nihlapp.core.models import User, Team, Club 
from django import forms
from django.contrib.auth.models import User
from nihlapp.core.models import Team, Club

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    team = models.ForeignKey(Team, verbose_name = "User's Team")
    club = models.ForeignKey(Club, verbose_name = "User's Club")
    email = models.EmailField("Email", max_length = 50)
    phone = models.CharField("Phone", max_length = 10)
    confirmation = models.CharField("Confirmation Key", max_length = 64, unique = True, blank = True, null = True)
    confirmed = models.NullBooleanField("Email Confirmed", default = False, blank = True, null = True)

    class Meta:
        app_label = "core"

    def __str__(self):
        return self.user.username

	def get_absolute_url(self):
		return "/%s/%s/%s" % ('users', 'detail', user.pk)
		
class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=30)
    firstName = forms.CharField(max_length=30)
    lastName = forms.CharField(max_length=30)
    group = forms.ModelChoiceField(label='Group', queryset=Group.objects.all().order_by('name'),initial=Team.objects.filter(pk=1))
    team = forms.ModelChoiceField(label='Team', queryset=Team.objects.all().order_by('name'))
    club = forms.ModelChoiceField(label='Club', queryset=Club.objects.all().order_by('name'))
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=10, required = False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True))
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(render_value=True))
    is_active = forms.BooleanField(label='Active', required = False)

    def __init__(self,club_id=None,team_id=None, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        if club_id:
		self.fields['club'].initial = Club.objects.get(pk=club_id)
	else:
		self.base_fields['club'].initial = Club.objects.filter(pk=1)
	if team_id:
		self.fields['club'].initial = Team.objects.get(pk=team_id)
	else:
		self.base_fields['team'].initial = Team.objects.filter(pk=1)

    
    def clean_username(self):
        data = self.cleaned_data['username']   
        # check if this username is available
        
        if self.initial == {}:
            try:
                checkUser = User.objects.get(username = data)
                raise forms.ValidationError("This username is not available, please choose a different username for your account.")
            except User.DoesNotExist:
                pass
        return data

    def clean(self):
        cleaned_data = self.cleaned_data
        
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords you have entered do not match. Please re-enter your password.")
        
        return cleaned_data

class SendInviteForm(forms.Form):
	name = forms.CharField(label="Name")
	email = forms.EmailField(label="Email")
	message = forms.CharField(label="Message", widget=forms.widgets.Textarea())
	club_id = forms.IntegerField(widget=forms.widgets.HiddenInput(),required = False)
	team_id = forms.IntegerField(widget=forms.widgets.HiddenInput(),required = False)
