'''
Created on February 11, 2010

@author: Mantas Vidutis
@author: Rick Matusiewicz

Version 0.0

Status:
    - the first version

To do:
    - features
    - stability

'''
import random
from django.db.models import Q
from nihlapp.core.models import Matchup, Season, EventType, Team as TeamModel

class Matchmaking:
    
    def __init__(self, newGameLimit, teams):
        
        # newGameLimit is the number of games to run,
        # teams is a list of local Team objects
        self.gameLimit = newGameLimit
        
        # start with a shuffled list
        self.teamList = random.shuffle(teams)
        self.storeMatches = False
        self.initMatchList
    
    def initMatchList(self):
        self.matchList = self.teams[:]
    
    def generate(self):
        self.storeMatches = True
        self.main()
    
    def recursiveMatch(self):
        x = self.gameLimit/len(self.teamList)
        while x > 0:
            self.teamList = random.shuffle(self.teamList)
            self.linearMatch()
        
    
    def linearMatch(self):
        for team in self.teamList:
            i = 0
            while i < self.gameLimit/2 & i < len(self.teams)/2:
                i += 1
                if self.teamList.index(team) + i + 1 >= len(self.teamList):
                    wrappedIndex = self.teamList.index(team) + i + 1
                    wrappedIndex -= len(self.teamList)
                    tempSlot = Slot(team.getTeamID(), self.teamList[wrappedIndex].getTeamID())
                    if team.setNextHomeSlot(tempSlot):
                        print "error setting home game for team " + team.getTeamID()
                    if self.teamList[wrappedIndex].setNextAwaySlot(tempSlot):
                        print "error setting away game for team " + self.teamList[wrappedIndex].getTeamID()
                else:
                    tempSlot = Slot(team.getTeamID, self.teamList[teams.index(team) + i + 1].getTeamID())
                    if team.setNextHomeSlot(tempSlot):
                        print "error setting home game for team " + team.getTeamID()
                    if self.teamList[wrappedIndex].setNextAwaySlot(tempSlot):
                        print "error setting away game for team " + self.teamList[teams.index(team) + i + 1].getTeamID()
                i += 1
    
    def main(self):
        currentTeam = None
        opponentTeam = None
        if ( len(self.teamList) > self.gameLimit ):
            self.linearMatch()
        else :
            self.recursiveMatch()
        return
        

class Team:
    def __init__(self,someName,someID,gameLimit):
        self.teamName = someName
        self.teamID = someID
        self.homeSched = []
        self.awaySched = []
        self.gameLimit = gameLimit
        self.homeIndex = None
        self.awayIndex = None
        self.initSchedules()
    
    def initSchedules(self):
        i = 0
        while (i < self.gameLimit):
            self.homeSched.append(None)
            self.awaySched.append(None)
            i += 2
        return
    
    def hasAwaySlotOpen():
        for x in self.awaySched:
            if x == None:
                return true
        return false
        
    def getName(self):
        return self.teamName
    
    def getTeamID(self):
        return self.teamID
    
    def getHomeSched(self):
        return self.homeSched
    
    def getAwaySched(self):
        return self.awaySched
    
    def getHomeSlot(self,ind):
        return self.homeSched[ind]
    
    def getAwaySlot(self,ind):
        return self.awaySched[ind]
    
    def setHomeSlot(self,ind,newSlot):
        self.homeSched[ind] = newSlot
    
    def setNextAwaySlot(self, newSlot):
        for x in self.homeSched:
            if x == None:
                x = newSlot
                return 0
        else: return 1
    
    def setNextAwaySlot(self, newSlot):
        for x in self.awaySched:
            if x == None:
                x = newSlot
                return 0
        else: return 1
    
    def setAwaySlot(self,ind,newSlot):
        self.awaySched[ind] = newSlot
    
    def display(self, storeMatches):
        #print "Matches for",self.teamName,"    length:",len(self.sched)
        self.slotInd = 0
        while(self.slotInd<len(self.sched)):
            if storeMatches:
                if self.sched[self.slotInd] is not None:
                    # do not store anything for "Pass" team
                    if self.teamID != 0:
                        self.sched[self.slotInd].store()
            else:
                if self.sched[self.slotInd] is not None:
                    self.sched[self.slotInd].display()
            self.slotInd += 1
    

  
class Slot:
    def __init__(self,newHome,newVisit):
        self.homeID = newHome
        self.visitorID = newVisit
        self.masked = False
    
    def store(self):
        # store team matchup
        try:
            matchup = Matchup()
            matchup.season = Season.objects.get(isCurrentSeason = True)
            
            if matchup.season.seasonStatus.name == "Scheduling Seeding Games":
                matchup.eventType = EventType.objects.get(name = "Seeding Game")
            else:
                matchup.eventType = EventType.objects.get(name = "Season Game")
            
            matchup.homeTeam = TeamModel.objects.get(id = self.homeID)
            matchup.awayTeam = TeamModel.objects.get(id = self.visitorID)
            matchup.save()
        except:
            # silently fail
            pass
    
    def mask(self):
        self.masked = True
    
    def display(self):
        pass
        #print "Home Team: ",self.homeID,"    Visiting Team: ",self.visitorID
    
