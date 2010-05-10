from django.http import Http404
from django.views.generic import list_detail
from nihlapp.core.models import Team, Division
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

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

def confirm(request, object_id):
				return render_to_response('core/division/confirm.html', {'object_id': object_id})

