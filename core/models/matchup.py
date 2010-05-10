from django.db import models
from nihlapp.core.models import Season, EventType, Team

class Matchup(models.Model):
    season = models.ForeignKey(Season, verbose_name = "Season")
    eventType = models.ForeignKey(EventType, verbose_name = "Event Type")
    homeTeam = models.ForeignKey(Team, verbose_name = "Home Team", related_name = "Matchup Home Team")
    awayTeam = models.ForeignKey(Team, verbose_name = "Away Team", related_name = "Matchup Away Team")

    class Meta:
        app_label = "core"

    def __str__(self):
        return "Matchup: %s v. %s" % (self.homeTeam, self.awayTeam)
