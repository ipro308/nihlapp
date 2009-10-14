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

# Season Statuses
# 1. Preparation [data entry - teams, etc]
# 2. Scheduling Seeding Games [teams set up seeding game schedules]
# 3. Seeding Games [seeding round is being played]
# 4. Scheduling Season Games [teams set up regular season game schedules]    
# 5. Season Games [season games are being played]
# 6. Completed [season has been completed, stats have been entered]
class SeasonStatus(models.Model):
    name = models.CharField("Season Status", max_length = 30, unique = True)    
    
    def __str__(self):
        return self.name

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
    seasonStatus = models.ForeignKey(SeasonStatus, verbose_name = "Season Status")

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

    def get_absolute_url(self):
        return "/%s/%s/%s" % ('accounts', 'detail', self.pk)

# Event Types
# 1. Seeding Game
# 2. Season Game
# 3. Practice Game
class EventType(models.Model):
    name = models.CharField("Event Type", max_length = 30, unique = True)
    
    def __str__(self):
        return self.name
    
# Event Statuses
# 1. Available [for scheduling]
# 2. Scheduled [another team picked this time]
# 3. Confirmed [home team confirmed game with away team]
# 4. Completed [stats entered]
class EventStatus(models.Model):
    name = models.CharField("Event Status", max_length = 30, unique = True)
    
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

    def __str__(self):
        return "%s vs. %s" % (self.homeTeam, self.awayTeam)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('events', 'detail', self.pk)

class Parameter(models.Model):
    name = models.CharField("Event Type Name", max_length = 30, unique = True)
    value = models.CharField("Event Type Name", max_length = 30)
    
    def __str__(self):
        return self.value
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('parameters', 'detail', self.pk)    
    
class EventStats(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
#    homeTeamGoals = models.PositiveSmallIntegerField("Home Team Goals")
#    awayTeamGoals = models.PositiveSmallIntegerField("Away Team Goals")
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

    def __str__(self):
        return "Event %s Stats" % (self.event)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventstats', 'detail', self.pk)
    
class EventGoal(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    team = models.ForeignKey(Team, verbose_name = "Team")
    player = models.PositiveSmallIntegerField("Player Number")
    period = models.PositiveSmallIntegerField("Period")
    time = models.TimeField("Time")
        
    def __str__(self):
        return "Event %s Goal by %s player %d" % (self.event, self.team, self.player)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventgoals', 'detail', self.pk)        
        
class PenaltyOffense(models.Model):
    name = models.CharField("Penalty Offense", max_length = 30)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('penaltyoffenses', 'detail', self.pk)    
        
        
class EventPenalty(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    team = models.ForeignKey(Team, verbose_name = "Team")
    player = models.PositiveSmallIntegerField("Player Number")
    period = models.PositiveSmallIntegerField("Period")
    penaltyTime = models.TimeField("Penalty Time")
    penaltyOffense = models.ForeignKey(PenaltyOffense, verbose_name = "Penalty Offense")
    timeOn = models.TimeField("Time ON")
    timeOff = models.TimeField("Time OFF")
    
    def __str__(self):
        return "Event %s Penalty for %s player %d" % (self.event, self.team, self.player)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventpenalties', 'detail', self.pk)       
    
class EventSuspension(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    team = models.ForeignKey(Team, verbose_name = "Team")
    player = models.PositiveSmallIntegerField("Player Number")
#    playerFirstName = models.CharField("Player's First Name", max_length = 30)
    playerLastName = models.CharField("Player's Last Name", max_length = 30)
    
    def __str__(self):
        return "Event %s Suspension for %s player %d" % (self.event, self.team, self.player)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventsuspensions', 'detail', self.pk)      
    
class EventGoalkeeperSaves(models.Model):
    event = models.ForeignKey(Event, verbose_name = "Event")
    team = models.ForeignKey(Team, verbose_name = "Team")
    player = models.PositiveSmallIntegerField("Player Number")
    firstPeriodSaves = models.PositiveSmallIntegerField("First Period Saves")
    secondPeriodSaves = models.PositiveSmallIntegerField("Second Period Saves")
    thirdPeriodSaves = models.PositiveSmallIntegerField("Third Period Saves")
    overtimeSaves = models.PositiveSmallIntegerField("Overtime Saves")

    def __str__(self):
        return "Event %s Goalkeeper Saves by %s player %d" % (self.event, self.team, self.player)
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('eventgoalkeepersaves', 'detail', self.pk)  


