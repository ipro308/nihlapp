from django.db import models
from nihlapp.core.models import *

class EventPenalty(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    team = models.ForeignKey(Team, verbose_name = "Team")
    player = models.PositiveSmallIntegerField("Player Number")
    period = models.PositiveSmallIntegerField("Period")
    penaltyTime = models.DateTimeField("Penalty Time")
    penaltyOffense = models.ForeignKey(PenaltyOffense, verbose_name = "Penalty Offense")
    timeOn = models.DateTimeField("Time ON")
    timeOff = models.DateTimeField("Time OFF")
    
    class Meta:
        app_label = "core"
    
    def __str__(self):
        return "Event %s Penalty for %s player %d" % (self.event, self.team, self.player)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventpenalties', 'detail', self.pk)