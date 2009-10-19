from django.db import models
from nihlapp.core.models import *

class Team(models.Model):
    name = models.CharField("Team Name", max_length = 30, unique = True)
    season = models.ForeignKey(Season, verbose_name = "Season")
    division = models.ForeignKey(Division, verbose_name = "Division")
    club = models.ForeignKey(Club, verbose_name = "Club")
    skillLevel = models.ForeignKey(SkillLevel, verbose_name = "Skill Level")
    #manager = models.ForeignKey(UserProfile, verbose_name = "Manager")
    #coach = models.ForeignKey(UserProfile, verbose_name = "Coach")
    managerName = models.CharField("Manager Name", max_length = 30)
    managerEmail = models.EmailField("Manager Email")
    coachName = models.CharField("Coach Name", max_length = 30, blank = True)
    coachEmail = models.EmailField("Coach Email", blank = True)

    class Meta:
        app_label = "core"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('teams', 'detail', self.pk)
    