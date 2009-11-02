from django.db import models
from django import forms
from django.contrib.auth.models import User, Group
from nihlapp.core.models import Team, Club

class Invitation(models.Model):
    key = models.CharField("Invitation Key", max_length = 64, unique = True)
    name = models.CharField("Full Name", max_length = 30)
    email = models.EmailField("Email")
    group = models.ForeignKey(Group, verbose_name = "Default Group")
    team = models.ForeignKey(Team, verbose_name = "Team")
    club = models.ForeignKey(Club, verbose_name = "Club")
    used = models.BooleanField("Used", default = False)

    class Meta:
        app_label = "core"
        
    def __str__(self):
        return "Invitation: %s" % (self.key)
    
class InvitationForm(forms.Form):
    username = forms.CharField(label = "Username", max_length = 30)
    password = forms.CharField(label = "Password", widget = forms.PasswordInput(render_value = False), min_length = 6, max_length = 30)
    password_confirm = forms.CharField(label = "Confirm Password", widget = forms.PasswordInput(render_value = False), min_length = 6, max_length = 30)
    
    def clean_username(self):
        data = self.cleaned_data['username']
        
        # check if this username is available
        try:
            checkUser = User.objects.get(username = data)
            raise forms.ValidationError("This username is not available, please choose a different username for your account.")
        except DoesNotExist, error:
            pass
        
        return data

    def clean(self):
        cleaned_data = self.cleaned_data
        
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords you have entered do not match. Please re-enter your password.")
        
        return cleaned_data