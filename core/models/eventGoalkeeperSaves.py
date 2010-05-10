from django.db import models
from nihlapp.core.models import Event, Team

class EventGoalkeeperSaves(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    team = models.ForeignKey(Team, verbose_name = "For Team", related_name = "Saves For Team")
    againstTeam = models.ForeignKey(Team, verbose_name = "Against Team", related_name = "Saves Against Team")
    player = models.PositiveSmallIntegerField("Player Number")
    firstPeriodSaves = models.PositiveSmallIntegerField("First Period Saves")
    secondPeriodSaves = models.PositiveSmallIntegerField("Second Period Saves")
    thirdPeriodSaves = models.PositiveSmallIntegerField("Third Period Saves")
    overtimeSaves = models.PositiveSmallIntegerField("Overtime Saves") 
    
    class Meta: 
        app_label = "core"
    
    def __str__(self):
        return "Event %s Goalkeeper Saves by %s player %d" % (self.event, self.team, self.player)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventgoalkeepersaves', 'detail', self.pk)