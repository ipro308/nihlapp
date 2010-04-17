# -*- coding: utf-8 -*-
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from nihlapp.core.models import Season, SeasonStatus, Division, SkillLevel, Team, Rink
from nihlapp.core.utils.Matchmaking import Matchmaking, Team as MatchmakingTeam
from django.shortcuts import get_object_or_404

@login_required
def list(request, pagination_id = 1):
    """
    TODO: This view does not seem to work anymore, the syntax seems correct and so does the logic
    however, the extra context variables are not being passed on to the template.
    Therefore, this view has been replaced with the one below called seasons_list. It works but pagination
    is not implmented yet
    """
    currentSeason = get_object_or_404(Season, isCurrentSeason = True)
    rinks_queryset = Rink.objects.all()
    foo_bar = "this sucks"
    
    return object_list(
                       request, 
                       queryset = Season.objects.all(), 
                       paginate_by = 20, 
                       allow_empty = True, 
                       page = pagination_id, 
                       template_name = 'core/season_list.html', 
                       extra_context = {'currentSeason':currentSeason, 'rinks_queryset':rinks_queryset, "foo_bar":foo_bar}
                       )

@login_required
def seasons_list(request):
    """
    TODO: Implement Pagination for this particular view
    """
    currentSeason = get_object_or_404(Season, isCurrentSeason = True)
    rinks_queryset = Rink.objects.all()
    object_list = Season.objects.all()
    allow_empty = True
    paginate_by = 20
    variables = RequestContext(request,{
				'currentSeason':currentSeason,
				'rinks_queryset':rinks_queryset,
				'object_list':object_list
				})
    return render_to_response('core/season_list.html',
				variables
				)

def confirm(request, season_id):
     print season_id;
     return render_to_response('core/season/confirm.html',{'user': request.user})

def stage1(request):
    
    if request.method == 'GET':
        return render_to_response('core/season/stage1.html', {'user': request.user})
    
    elif request.method == 'POST':
        errorMessage = False
        
        # change season status
        currentSeason = Season.objects.get(isCurrentSeason = True)
        currentSeason.seasonStatus = SeasonStatus.objects.get(name = "Scheduling Seeding Games")
        currentSeason.save()
        
        # generate team matches (for seeding games)
        try:
            divisions = Division.objects.all()
            skillLevels = SkillLevel.objects.all()
            # go through every division and skill level
            for division in divisions:
                for skillLevel in skillLevels:
                    teams = []
                    querySet = Team.objects.filter(season = Season.objects.get(isCurrentSeason = True), 
                                                   division = division, 
                                                   skillLevel = skillLevel)
                    for team in querySet:
                        teams.append(MatchmakingTeam(team.name, team.id, 8))
                            
                    # todo: move number 8 to a parameter.
                    
                    print "creating matchmaking object"
                    makeMe = Matchmaking(8, teams) 
                    
                    print "matching teams"
                    makeMe.generate()
                    print "teams matched"
        except Exception, error:
            print error
            errorMessage = "Error has occured while matchmaking teams: %s." % error
        
        return render_to_response('core/season/stage1_done.html', {'user': request.user, 'errorMessage': errorMessage})

def stage2(request):
    
    if request.method == 'GET':
        return render_to_response('core/season/stage2.html', {'user': request.user})
    
    elif request.method == 'POST':
        # change season status
        currentSeason = Season.objects.get(isCurrentSeason = True)
        currentSeason.seasonStatus = SeasonStatus.objects.get(name = "Seeding Games")
        currentSeason.save()
        return render_to_response('core/season/stage2_done.html', {'user': request.user})

def stage3(request):
    
    if request.method == 'GET':
        return render_to_response('core/season/stage3.html', {'user': request.user})
    
    elif request.method == 'POST':
        errorMessage = False
        
        # change season status
        currentSeason = Season.objects.get(isCurrentSeason = True)
        currentSeason.seasonStatus = SeasonStatus.objects.get(name = "Scheduling Season Games")
        currentSeason.save()
        
        # generate team matches (for season games)
        try:
            divisions = Division.objects.all()
            skillLevels = SkillLevel.objects.all()
            # go through every division and skill level
            for division in divisions:
                for skillLevel in skillLevels:
                    teamList = list()
                    querySet = Team.objects.filter(season = Season.objects.get(isCurrentSeason = True), 
                                                   division = division, 
                                                   skillLevel = skillLevel)
                    for team in querySet:
                        teamList.append(MatchmakingTeam(team.name, team.id, 8))
                            
                    # todo: move number 8 to a parameter.
                    makeMe = Matchmaking(8, teamList) 
                    makeMe.generate()
        except Exception, error:
            errorMessage = "Error has occured while matchmaking teams: %s." % error
        
        return render_to_response('core/season/stage3_done.html', {'user': request.user, 'errorMessage': errorMessage})

def stage4(request):
    
    if request.method == 'GET':
        return render_to_response('core/season/stage4.html', {'user': request.user})
    
    elif request.method == 'POST':
        # change season status
        currentSeason = Season.objects.get(isCurrentSeason = True)
        currentSeason.seasonStatus = SeasonStatus.objects.get(name = "Season Games")
        currentSeason.save()
        return render_to_response('core/season/stage4_done.html', {'user': request.user})

def stage5(request):
    
    if request.method == 'GET':
        return render_to_response('core/season/stage5.html', {'user': request.user})
    
    elif request.method == 'POST':
        # change season status
        currentSeason = Season.objects.get(isCurrentSeason = True)
        currentSeason.seasonStatus = SeasonStatus.objects.get(name = "Completed")
        currentSeason.save()
        return render_to_response('core/season/stage5_done.html', {'user': request.user})

