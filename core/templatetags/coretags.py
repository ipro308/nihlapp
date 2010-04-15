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
def teamCount(input, args):
        list = eval(str(args))
        #a = [int(s) for s in str(args).split()]
        #team_count = Team.objects.filter(club__id = input, division = a[0], skillLevel = a[1]).count()
        return list

@register.filter("argCrap")
def argCrap(arg1, arg2):
        test = '[' + str(arg1) + ', ' + str(arg2) + ']'
        return str(test)

