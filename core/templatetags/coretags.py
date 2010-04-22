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
def teamCount(clubId, divLev):
        #list = eval(str(divLev));
        #test = [int(s) for s in str(divLev).split(":")]
        #a, _, b = str(divLev).partition(" ")
        #test = [a, b]
        #print "divLev = " + str(divLev)
        #print "test = " + str(test)
        #print "test[0] = " + str(test[0])
        #print "test[1] = " + str(test[1])
        #team_count = Team.objects.filter(club__id = clubId, division = test[0], skillLevel = test[1]).count()
        print divLev
        return divLev
        #return a + " - " + b
        #return "a: " + a + " --b: " + b + " --tc: " + str(team_count) + " .."

@register.filter("listBuild")
def listBuild(division, level):
        test = '[' + str(division) + ', ' + str(level) + ']'
        testTwo = str(division)+":"+str(level)
        li = [division, level]
        return str(testTwo)

