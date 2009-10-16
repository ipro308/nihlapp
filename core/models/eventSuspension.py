from django.db import models
from nihlapp.core.models import *

class EventSuspension(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    team = models.ForeignKey(Team, verbose_name = "Team")
    player = models.PositiveSmallIntegerField("Player Number")
# playerFirstName = models.CharField("Player's First Name", max_length = 30)
    playerLastName = models.CharField("Player's Last Name", max_length = 30)
    
    class Meta:
        app_label = "core"
    
    def __str__(self):
        return "Event %s Suspension for %s player %d" % (self.event, self.team, self.player)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventsuspensions', 'detail', self.pk)