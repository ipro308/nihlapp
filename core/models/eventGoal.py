from django.db import models
from nihlapp.core.models import *

class EventGoal(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    team = models.ForeignKey(Team, verbose_name = "For Team", related_name = "Goal For Team")
    againstTeam = models.ForeignKey(Team, verbose_name = "Against Team", related_name = "Goal Against Team")
    player = models.PositiveSmallIntegerField("Player Number")
    period = models.PositiveSmallIntegerField("Period")
    time = models.DateTimeField("Time")
        
    class Meta:
        app_label = "core"
        
    def __str__(self):
        return "Event %s Goal by %s player %s" % (self.event, self.team, self.player)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventgoals', 'detail', self.pk)