from django import template
from django.template import RequestContext
from django.http import *
from django.shortcuts import render_to_response
from nihlapp.core.models import Club, Team
import re

register = template.Library()

@register.filter
def formatPeriod(input):
    try:
        return {1: lambda: "1st Period",
                2: lambda: "2nd Period",
                3: lambda: "3rd Period",
                4: lambda: "Overtime"
                }[input]()
    except KeyError:
        return None

@register.filter
def numberStrip(input): 
        """Function to strip the number (ex. #1) 
        from the team name to avoid duplicate images.
        """
        p = re.compile( '\ #[0-9]')
        output = p.sub( '', input)
        p = re.compile( '\ ')
        output = p.sub('', output)
        return output
 
#what i'm trying to do:
#split the array apart and use it as two arguments, but it ain't working
@register.filter("teamCount")
def teamCount(divLev, clubId):
        #print "div\tLev\tclubF\ttest"
        test = [int(s) for s in str(divLev).split("s")]
        #print str(test[0]) + "\t" + str(test[1]) + "\t" + str(test[2]) + "\t" + str(test) + "\n--\n"
        #print test
        if test[2] == clubId:
            team_count = Team.objects.filter(club__id = clubId, division = test[0], skillLevel = test[1]).count()
        elif test[2] == 0:
             team_count = Team.objects.filter(club__id = clubId, division = test[0], skillLevel = test[1]).count()
        else:
             team_count = 0
        #print "tc: " + str(team_count)
        return team_count

@register.filter("addClub")
def addClub(divLev, clubId):
        #print str(divLev) + "s" + str(clubId)
        return str(divLev) + "s" + str(clubId)

@register.filter("listBuild")
def listBuild(division, level):
        #test = '[' + str(division) + ', ' + str(level) + ']'
        testTwo = str(division) + "s" + str(level)
        #print "div\tlev\tt2\tli"
        #print str(division) + "\t" + str(level) + "\t" + str(testTwo) + "\t" + str(li) + ""
        return testTwo

