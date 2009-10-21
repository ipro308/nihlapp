from nihlapp.core.models import *
from django.db.models import Count, Q, Sum
from time import strptime, strftime

class TeamStats(Team):

    class Meta:
        proxy = True

    ## Returns stats for this team in a given season.
    # @todo filter by season
    #
    # @param  self      This object.
    # @param  season    [Optional] season to retrieve stats for.
    #
    # @return dict
    def get_stats(self, season = None):
        team = self
        result = {}
        # use current season if season was not specified
        if season == None:
            season = Season.objects.get(isCurrentSeason = True)
            
        completedEvent = EventStatus.objects.get(name = 'Completed')
        
        result['teamId'] = team.id
        result['teamName'] = team.name
        result['gamesPlayed'] = Event.objects.filter((Q(homeTeam = team) | Q(awayTeam = team)) & 
                                                      Q(eventStatus = completedEvent)).count()
                                                      
        result['wins'] = EventStats.objects.filter((Q(event__homeTeam = team) | Q(event__awayTeam = team)) & 
                                                    Q(event__eventStatus = completedEvent) & 
                                                    Q(winner = team)).count()
                                                    
        result['losses'] = EventStats.objects.filter((Q(event__homeTeam = team) | Q(event__awayTeam = team)) & 
                                                      Q(event__eventStatus = completedEvent) &
                                                      Q(loser = team)).count()
                                                    
        result['ties'] = EventStats.objects.filter((Q(event__homeTeam = team) | Q(event__awayTeam = team)) & 
                                                    Q(event__eventStatus = completedEvent) &
                                                    Q(tie = True)).count()
        # two points for win, one point for tie
        result['points'] = 2 * result['wins'] + result['ties']
        result['goalsFor'] = EventGoal.objects.filter(Q(team = self)).count()
        result['goalsAgainst'] = EventGoal.objects.filter(Q(againstTeam = self)).count()
        result['plusMinus'] = result['goalsFor'] - result['goalsAgainst']
        
        q = EventGoalkeeperSaves.objects.filter(Q(againstTeam = self)).aggregate(Sum('firstPeriodSaves'), 
                                                                                 Sum('secondPeriodSaves'), 
                                                                                 Sum('thirdPeriodSaves'), 
                                                                                 Sum('overtimeSaves'))

        if q['firstPeriodSaves__sum'] != None:
            result['shotsOnGoal'] = q['firstPeriodSaves__sum'] + q['secondPeriodSaves__sum'] + q['thirdPeriodSaves__sum'] + q['overtimeSaves__sum']
        else: 
            result['shotsOnGoal'] = 0
        
        
        result['totalPenaltyMinutes'] = float(0)
        qs = EventPenalty.objects.filter(Q(team = self))
        for object in qs:
            result['totalPenaltyMinutes'] = result['totalPenaltyMinutes'] + float(strftime("%M", object.penaltyTime.timetuple())) + float(strftime("%S", object.penaltyTime.timetuple())) / 60
        
        result['totalPenaltyMinutes'] = round(result['totalPenaltyMinutes'], 1)
        
        # make sure division by zero does not occur
        if result['gamesPlayed'] != 0:
            result['goalsForAverage'] = float(result['goalsFor'] / result['gamesPlayed'])
            result['goalsAgainstAverage'] = float(result['goalsAgainst'] / result['gamesPlayed'])
            result['average'] = float(result['points'] / result['gamesPlayed'])
        else:
            result['goalsForAverage'] = float(0)
            result['goalsAgainstAverage'] = float(0)            
            result['average'] = float(0)
        
        return result
