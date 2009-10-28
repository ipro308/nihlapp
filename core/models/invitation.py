from django.db import models
from django import forms
from django.contrib.auth.models import Group
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
    