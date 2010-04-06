# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import list_detail
from nihlapp.core.models import Team, Event, EventStats
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from nihlapp.core.models.team import CreateTeamForm
from django.db.models import Q


def detail(request, team_id):

    # Look up the publisher (and raise a 404 if it can't be found).
    try:
        schedule_queryset = Event.objects.filter(Q(homeTeam__id = team_id) | Q(awayTeam__id = team_id)).order_by('dateTimeEvent')
        stats_queryset = EventStats.objects.filter(Q(event__homeTeam__id = team_id) | Q(event__awayTeam__id = team_id))
        winner = EventStats.objects.filter(winner = team_id).count()
        loser = EventStats.objects.filter(loser = team_id).count()
    except: 
        raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_detail(
        request,
        queryset = Team.objects.all(),
        template_name = "core/team_detail.html",
        template_object_name = "object",
        object_id = team_id,
        extra_context = {"schedule_queryset" : schedule_queryset, "stats_queryset" : stats_queryset, "winner" : winner, "loser" : loser}
    )
    
def create_team(request):
	msg = ''
	if request.method == 'POST':
		form = CreateTeamForm(request.POST)
		if form.is_valid():
			new_team = form.save()
			msg = "Team succesfully created."
			print("post submit %s" % (request.POST['submit']))
			if request.POST['submit'] == u'addmanager':
				print("redirect to account creation")
				return HttpResponseRedirect('/accounts/create')
			else:
				print("return to teams list display")
				print("team id: %s" % new_team.id)
				return HttpResponseRedirect(reverse('nihlapp.core.views.teams.detail', args=(new_team.id,)))
	form = CreateTeamForm()
	return render_to_response('core/custom_forms/team_create_form.html',{'form': form})
