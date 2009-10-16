from django.db import models
from nihlapp.core.models import *

class Season(models.Model):
    year = models.CharField("Season Year", max_length = 4, unique = True) # essentially the name
    seedingBeginDate = models.DateField("Seeding Begin Date")
    seedingSchedDeadline = models.DateField("Seeding Schedule Deadline")
    seedingStatDeadline = models.DateField("Seeding Stat Deadline")
    seasonBeginDate = models.DateField("Season Begin Date")
    seasonSchedDeadline = models.DateField("Season Schedule Deadline")
    seasonStatDeadline = models.DateField("Season Stat Deadline")
    seasonEnd = models.DateField("Season Ends")
    isCurrentSeason = models.BooleanField("Is Current Season")
    seasonStatus = models.ForeignKey(SeasonStatus, verbose_name="Status")

    class Meta:
		app_label = "core"

    def __str__(self):
        return "%s Season" % (self.year)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('seasons', 'detail', self.pk)