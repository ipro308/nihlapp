from django.http import Http404
from django.views.generic import list_detail
from nihlapp.core.models import Team, Event, EventStats

def detail(request, team_id):

    # Look up the publisher (and raise a 404 if it can't be found).
    try:
        schedule_queryset = Event.objects.filter(homeTeam__id = team_id)
        stats_queryset = EventStats.objects.filter(event__homeTeam__id = object_id )
    except: 
        raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Team.objects.all(),
        template_name = "core/team_detail.html",
        template_object_name = "object",
        object_id = team_id,
        extra_context = {"schedule_queryset" : schedule_queryset, "stats_queryset" : stats_queryset}
    )
