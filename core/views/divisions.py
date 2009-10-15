from django.http import Http404
from django.views.generic import list_detail
from nihlapp.core.models import Team, Division

def detail(request, object_id):

    # Look up the publisher (and raise a 404 if it can't be found).
    try:
    	team_queryset = Team.objects.filter(division__id = object_id)
    except: 
        raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Division.objects.all(),
        object_id = object_id,
        extra_context = {"team_queryset" : team_queryset}
    )
