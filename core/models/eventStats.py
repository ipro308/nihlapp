from django.db import models
from nihlapp.core.models import Event, Team

class EventStats(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    majorPenaltiesAssessed = models.BooleanField("Major Penalties Assessed")
    referee1Name = models.CharField("Referee #1 Name", max_length = 30)
    referee2Name = models.CharField("Referee #2 Name", max_length = 30)
    referee3Name = models.CharField("Referee #3 Name", max_length = 30)
    referee1Level = models.CharField("Referee #1 Level", max_length = 30)
    referee2Level = models.CharField("Referee #2 Level", max_length = 30)
    referee3Level = models.CharField("Referee #3 Level", max_length = 30)
    referee1IHOANum = models.CharField("Referee #1 IHOA Number", max_length = 30)
    referee2IHOANum = models.CharField("Referee #2 IHOA Number", max_length = 30)
    referee3IHOANum = models.CharField("Referee #3 IHOA Number", max_length = 30)
    winner = models.ForeignKey(Team, verbose_name = "Winning Team", related_name = "Winning Team", blank = True, null = True)
    loser = models.ForeignKey(Team, verbose_name = "Losing Team", related_name = "Losing Team", blank = True, null = True)
    tie = models.BooleanField("Tie", default = False)
    
    class Meta:
		app_label = "core"
    
    def __str__(self):
        return "Event %s Stats" % (self.event)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventstats', 'detail', self.pk)