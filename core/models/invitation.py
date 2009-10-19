from django.db import models
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
        