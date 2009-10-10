from django.db import models
from django import forms
from django.contrib.auth.models import User
#from time import strftime
from nihlapp.core.models import *

#
# nihl application models
#

class Club(models.Model):
    name = models.CharField("Club Name", max_length = 30, unique = True)
	#contact = models.ForeignKey(UserProfile, "Contact")
    contactName = models.CharField("Contact Name", max_length = 30, blank = True)
    contactEmail = models.EmailField("Contact Email", blank = True)
    address = models.CharField("Address", max_length = 30, blank = True)
    city = models.CharField("City", max_length = 30, blank = True)
    state = models.CharField("State", max_length = 2, blank = True)
    zip = models.CharField("Zipcode", max_length = 5, blank = True)    

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('clubs', 'detail', self.pk)

class Division(models.Model):
    name = models.CharField("Division Name", max_length = 30, unique = True)
	#num_teams = models.IntegerField("Number of Teams")
	#contact = models.ForeignKey(UserProfile, "Contact")
    contactName = models.CharField("Contact Name", max_length = 30, blank = True)
    contactEmail = models.EmailField("Contact Email", blank = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('divisions', 'detail', self.pk)

class Season(models.Model):
    year = models.CharField("Season Year", max_length = 4, unique = True) # essentially the name
    seedingBeginDate = models.DateField("Seeding Begin Date")
    seedingSchedDeadline = models.DateField("Seeding Schedule Deadline")
    seedingStatDeadline = models.DateField("Seeding Stat Deadline")
    seasonBeginDate = models.DateField("Season Begin Date")
    seasonSchedDeadline = models.DateField("Season Schedule Deadline")
    seasonStatDeadline = models.DateField("Season Stat Deadline")
    seasonEnd = models.DateField("Season Ends")
	#isCurrentSeason = models.BooleanField("Is Current Season")

    def __str__(self):
        return "%s Season" % (self.year)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('seasons', 'detail', self.pk)

class SkillLevel(models.Model):
    name = models.CharField("Skill Level Name", max_length = 30, unique = True)
    weight = models.PositiveSmallIntegerField("Weight", unique = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('skilllevels', 'detail', self.pk)

class Team(models.Model):
    name = models.CharField("Team Name", max_length = 30, unique = True)
    season = models.ForeignKey(Season, verbose_name = "Season")
    division = models.ForeignKey(Division, verbose_name = "Division")
    club = models.ForeignKey(Club, verbose_name = "Club")
    skillLevel = models.ForeignKey(SkillLevel, verbose_name = "Skill Level")
	#manager = models.ForeignKey(UserProfile, verbose_name = "Manager")
	#coach = models.ForeignKey(UserProfile, verbose_name = "Coach")
	managerName = models.CharField("Manager Name", max_length = 30)
    managerEmail = models.EmailField("Manager Email")
    coachName = models.CharField("Coach Name", max_length = 30, blank = True)
    coachEmail = models.EmailField("Coach Email", blank = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('teams', 'detail', self.pk)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    team = models.ForeignKey(Team, verbose_name = "User's Team")
    club = models.ForeignKey(Club, verbose_name = "User's Club")
    email = models.EmailField("Email", max_length = 30)
    phone = models.CharField("Phone", max_length = 10)

    def __str__(self):
        return self.user.username

class EventType(models.Model):
    name = models.CharField("Event Type Name", max_length = 30, unique = True)
    
class EventStatus(models.Model):
    name = models.CharField("Event Status Name", max_length = 30, unique = True)
    
class Rink(models.Model):
    name = models.CharField("Rink Name", max_length = 30, unique = True)
    address = models.CharField("Address", max_length = 30, blank = True)
    city = models.CharField("City", max_length = 30, blank = True)
    state = models.CharField("State", max_length = 2, blank = True)
    zip = models.CharField("Zipcode", max_length = 5, blank = True)
    contactName = models.CharField("Contact Name", max_length = 30, blank = True)
    contactEmail = models.EmailField("Contact Name", max_length = 30, blank = True)
	#contactPhone = models.CharField("Contact Phone Number", max_length = 15, blank = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('rinks', 'detail', self.pk)    
    
class Event(models.Model):
    dateTimeEvent = models.DateTimeField("Event Date and Time")
    dateTimeScheduled = models.DateTimeField("Scheduled Timestamp")
    dateTimeConfirmed = models.DateTimeField("Confirmed Timestamp")
    dateTimeCancelled = models.DateTimeField("Cancelled Timestamp")
    eventType = models.ForeignKey(EventType, verbose_name = "Event Type")
    eventStatus = models.ForeignKey(EventStatus, verbose_name = "Event Status")
    homeTeam = models.ForeignKey(Team, verbose_name = "Home Team", related_name = "Home Team")
    awayTeam = models.ForeignKey(Team, verbose_name = "Away Team", related_name = "Away Team")
    rink = models.ForeignKey(Rink, verbose_name = "Rink")
    season = models.ForeignKey(Season, verbose_name = "Season")

    def __str__(self):
        return self.dateTimeEvent
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('events', 'detail', self.pk)

class Parameter(models.Model):
    name = models.CharField("Event Type Name", max_length = 30, unique = True)
    value = models.CharField("Event Type Name", max_length = 30)
    
class EventStats(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    homeTeamGoals = models.PositiveSmallIntegerField("Home Team Goals")
    awayTeamGoals = models.PositiveSmallIntegerField("Away Team Goals")
    teamHome = models.ForeignKey(Team, verbose_name = "Home Team")
    teamAway = models.ForeignKey(Team, verbose_name = "Away Team")
    
    def __str__(self):
        return "Event %s Stats" % (self.event)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventstats', 'detail', self.pk)
    