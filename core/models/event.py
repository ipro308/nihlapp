from django.db import models
from nihlapp.core.models import EventType, EventStatus, Team, Rink, Season
from time import strftime

class Event(models.Model):
    dateTimeEvent = models.DateTimeField("Event Date and Time")
    dateTimeCreated = models.DateTimeField("Created Timestamp", blank = True, null = True)
    dateTimeScheduled = models.DateTimeField("Scheduled Timestamp", blank = True, null = True)
    dateTimeConfirmed = models.DateTimeField("Confirmed Timestamp", blank = True, null = True)
    dateTimeCancelled = models.DateTimeField("Cancelled Timestamp", blank = True, null = True)
    eventType = models.ForeignKey(EventType, verbose_name = "Event Type")
    eventStatus = models.ForeignKey(EventStatus, verbose_name = "Event Status")
    homeTeam = models.ForeignKey(Team, verbose_name = "Home Team", related_name = "Home Team")
    awayTeam = models.ForeignKey(Team, verbose_name = "Away Team", related_name = "Away Team", blank = True, null = True)
    rink = models.ForeignKey(Rink, verbose_name = "Rink")
    season = models.ForeignKey(Season, verbose_name = "Season")

    class Meta:
        app_label = "core"

    def __str__(self):
        return strftime("%m/%d/%Y %I:%M %p", self.dateTimeEvent.timetuple())
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('stats', 'event', self.pk)
