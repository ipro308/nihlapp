from django.db import models
from nihlapp.core.models import *

class EventStats(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    majorPenaltiesAssessed = models.BooleanField("Major Penalties Assessed")
    referee1Name = models.CharField("Event Type Name", max_length = 30)
    referee2Name = models.CharField("Event Type Name", max_length = 30)
    referee3Name = models.CharField("Event Type Name", max_length = 30)
    referee1Level = models.CharField("Event Type Name", max_length = 30)
    referee2Level = models.CharField("Event Type Name", max_length = 30)
    referee3Level = models.CharField("Event Type Name", max_length = 30)
    referee1IHOANum = models.CharField("Event Type Name", max_length = 30)
    referee2IHOANum = models.CharField("Event Type Name", max_length = 30)
    referee3IHOANum = models.CharField("Event Type Name", max_length = 30)
    
    class Meta:
		app_label = "core"
    
    def __str__(self):
        return "Event %s Stats" % (self.event)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventstats', 'detail', self.pk)