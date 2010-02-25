from django.db import models
from nihlapp.core.models import SeasonStatus

class Season(models.Model):
    year = models.CharField("Season Year", max_length = 4, unique = True) # essentially the name
    seedingBeginDate = models.DateField("Seeding Begin Date (YYYY-MM-DD)")
    seedingSchedDeadline = models.DateField("Seeding Schedule Deadline (YYYY-MM-DD)")
    seedingStatDeadline = models.DateField("Seeding Stat Deadline (YYYY-MM-DD)")
    seasonBeginDate = models.DateField("Season Begin Date (YYYY-MM-DD)")
    seasonSchedDeadline = models.DateField("Season Schedule Deadline (YYYY-MM-DD)")
    seasonStatDeadline = models.DateField("Season Stat Deadline (YYYY-MM-DD)")
    seasonEnd = models.DateField("Season Ends (YYYY-MM-DD)")
    isCurrentSeason = models.BooleanField("Current Season")
    seasonStatus = models.ForeignKey(SeasonStatus, verbose_name="Status")

    class Meta:
        app_label = "core"

    def __str__(self):
        return "%s Season" % (self.year)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('seasons', 'detail', self.pk)
    
    def save(self, *args, **kwargs):
        if self.isCurrentSeason == True:
            # mark other seasons as not current
            seasons = Season.objects.filter(isCurrentSeason = True)
            for season in seasons:
                season.isCurrentSeason = False
                season.save()
        elif self.isCurrentSeason == False:
            # make sure there is another current season, or set this one back to current
            try:
                Season.objects.get(isCurrentSeason = True)
            except Season.DoesNotExist:
                self.isCurrentSeason == True

        super(Season, self).save(*args, **kwargs)