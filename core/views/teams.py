# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import list_detail
from nihlapp.core.models import Team, Event, EventStats
from nihlapp.core.models.team import CreateTeamForm
from django.shortcuts import render_to_response

def detail(request, team_id):

    # Look up the publisher (and raise a 404 if it can't be found).
    #try:
        #schedule_queryset = Event.objects.filter(homeTeam__id = team_id)
        #stats_queryset = EventStats.objects.filter(event__homeTeam__id = object_id )
    #except: 
     #   raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Team.objects.all(),
        template_name = "core/team_detail.html",
        template_object_name = "object",
        object_id = team_id,
        extra_context = {"schedule_queryset" : list(), "stats_queryset" : list()}
    )

def create_team(request):
	msg = ''
	if request.method == 'POST':
		form = CreateTeamForm(request.POST)
		if form.is_valid():
			form.save()
			msg = "Team succesfully created."
			if POST['submit'] == 'add manager':
				HttpResponseRedirect('/accounts/create')		
	else:
		form = CreateTeamForm()
	return render_to_response('core/custom_forms/team_create_form.html',{'form': form})
