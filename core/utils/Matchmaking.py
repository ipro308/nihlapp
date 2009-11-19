'''
Created on Nov 18, 2009

@author: Dustin Barksdale

Version: 1.3

STATUS:
    -schedules are coordinated so as to preserve schedule slots of other teams
        +passes are not yet dealt with
    -away/home distribution will be uneven for small divisions
    -Matchmaking.__init__() is currently adjusted for testing purposes
        +final version will pull data from data tables
    -Various print statements exist for debugging purposes.
            These will be removed later.

TO DO:
    -read from tables
    -write to tables
    -fix handling of passes
'''
import random

class Matchmaking:
    #currently configured for testing
    def __init__(self,newGameLimit):
        self.gameLimit = newGameLimit
        self.teamList = [Team("Team 1",1,self.gameLimit),Team("Team 2",2,self.gameLimit),Team("Team 3",3,self.gameLimit)]
        self.matchList = self.teamList[:]
        self.numTeams = -1
        self.passTeam = Team("Pass",0,self.gameLimit)
        
    def initMatchList(self):
        self.matchList = self.teamList[:]

    #test behavior for an odd number of teams
    def testMe(self):
        self.numTeams = 3
        self.main()

    ''' 
     For now, only regular scheduling (ie. no playoff scheduling)
     Distribution of home/away games is not entirely balanced
    '''
    
    def main(self):
        currentTeam = None
        opponentTeam = None
        numRdyTeams = 0
        slotCounter = 0

        if(self.numTeams<2):
            return None
    
        #run through schedule
        while(slotCounter<self.gameLimit):
            numRdyTeams = 0
            #run through all teams
            while(numRdyTeams<self.numTeams):
                currentTeam = random.choice(self.teamList)
                ''' print output for testing purposes '''
                print "current team:",self.teamList.index(currentTeam)
                #if current team has no match in current slot
                if(currentTeam.getSlot(slotCounter)==None):
                    opponentTeam = currentTeam
                    #prevent team from being matched with itself or a team already scheduled
                    while((currentTeam==opponentTeam) or (opponentTeam.getSlot(slotCounter)!=None)):
                        #if current team is the last one left, give it a pass for now
                        if(numRdyTeams==(self.numTeams-1)):
                            self.teamList[self.teamList.index(currentTeam)].incPasses()
                            opponentTeam = self.passTeam
                        else:
                            opponentTeam = random.choice(self.teamList)
                    #set match into current team's schedule
                    self.teamList[self.teamList.index(currentTeam)].setSlot(slotCounter,Slot(currentTeam.teamID,opponentTeam.teamID))
                    numRdyTeams += 1
                    #set match into opponent's schedule
                    if(opponentTeam!=self.passTeam):
                        self.teamList[self.teamList.index(opponentTeam)].setSlot(slotCounter,Slot(currentTeam.teamID,opponentTeam.teamID))
                        numRdyTeams += 1
                    ''' print output for testing purposes '''
                    print "team set"
            ''' print output for testing purposes '''
            print "Slot #",(slotCounter+1),"set"
            slotCounter += 1
        
        ''' fill-in passes with random matches
        numRdyTeams = 0
        maxPasses = self.passTeam
        tempPasses = 0
        #find out who has the most passes
        while numRdyTeams < len(self.teamList):
            tempPasses = self.teamList[numRdyTeams].getPasses()
            if(tempPasses > maxPasses):
                maxPasses = tempPasses
            numRdyTeams += 1
        #print output for testing purposes
        print "Max passes: ",maxPasses
        #append every team to accommodate extra matches
        numRdyTeams = 0
        while numRdyTeams < len(self.teamList):
            tempPasses = 0
            while(tempPasses<maxPasses):
                self.teamList[numRdyTeams].appSched(None)
                tempPasses += 1
            #print output for testing purposes
            print "new schedule length:",len(self.teamList[numRdyTeams].getSched())
            numRdyTeams += 1
        #start slotCounter at head of extra matches
        slotCounter = self.gameLimit
        #print output for testing purposes
        print "new game limit",self.gameLimit+maxPasses
        #fill in extra matches at random
        while(slotCounter<(self.gameLimit+maxPasses)):
            while():
                self.teamList
        '''
        
        #print schedules for each team
        numRdyTeams = 0
        while (numRdyTeams < len(self.teamList)):
            self.teamList[numRdyTeams].display()
            numRdyTeams += 1


class Team:
    def __init__(self,someName,someID,gameLimit):
        self.teamName = someName
        self.teamID = someID
        self.sched = []
        self.gameLimit = gameLimit
        self.slotInd = None
        self.numPasses = 0
        ''' initialize schedule '''
        initSched = 0
        while (initSched<gameLimit):
            self.sched.append(None)
            initSched += 1
         
    def getName(self):
        return self.teamName
    
    def getTeamID(self):
        return self.teamID
    
    def getSched(self):
        return self.sched
    
    def getSlot(self,ind):
        return self.sched[ind]
    
    def getPasses(self):
        return self.numPasses
    
    def setSlot(self,ind,newSlot):
        self.sched[ind] = newSlot
        
    def incPasses(self):
        self.numPasses += 1
    
    def appSched(self,newSlot):
        self.sched.append(newSlot)
    
    def display(self):
        print "Matches for",self.teamName,"    length:",len(self.sched)
        self.slotInd = 0
        while(self.slotInd<len(self.sched)):
            self.sched[self.slotInd].display()
            self.slotInd += 1
        
class Slot:    
    def __init__(self,newHome,newVisit):
        self.homeID = newHome
        self.visitorID = newVisit
        
    def display(self):
        print "Home Team: ",self.homeID,"    Visiting Team: ",self.visitorID

''' Test section '''

makeMe = Matchmaking(8)
makeMe.testMe()

''' End test section '''