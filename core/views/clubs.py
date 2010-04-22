from django.http import Http404
from django.views.generic import list_detail
from nihlapp.core.models import Club, Team
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

def detail(request, object_id):

    # Look up the publisher (and raise a 404 if it can't be found).
    try:
								team_queryset = Team.objects.filter(club__id = object_id)
								team_count = Team.objects.count()
    except: 
								raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Club.objects.all(),	
        template_name = "core/club_detail.html",
        template_object_name = "object",
        object_id = object_id,
        extra_context = {"team_queryset" : team_queryset, "team_count" : team_count}
    )

def confirm(request, object_id):
    return render_to_response('core/club/confirm.html', {'object_id': object_id})

