from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from nihlapp.core.models import Season, SeasonStatus, Division, SkillLevel, Team, Rink
from nihlapp.core.utils.Matchmaking import Matchmaking, Team as MatchmakingTeam

@login_required
def list(request, pagination_id = 1):
    
    currentSeason = Season.objects.get(isCurrentSeason = True)
    rinks_queryset = Rink.objects.all()
    
    return object_list(
                       request, 
                       queryset = Season.objects.all(), 
                       paginate_by = 20, 
                       allow_empty = True, 
                       page = pagination_id, 
                       template_name = 'core/season_list.html', 
                       extra_context = {'currentSeason' : currentSeason, 'rinks_queryset' : rinks_queryset}
                       )

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
                    makeMe = Matchmaking(8, teams) 
                    makeMe.generate()
        except Exception, error:
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

