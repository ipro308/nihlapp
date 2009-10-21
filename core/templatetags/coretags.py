from django import template

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
    
