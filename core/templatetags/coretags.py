from django import template
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
        
    
