from django.http import Http404
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from nihlapp.core.models import Season, SeasonStatus

@login_required
def list(request, pagination_id = 1):
    
    currentSeason = Season.objects.get(isCurrentSeason = True)
    
    return object_list(
                       request, 
                       queryset = Season.objects.all(), 
                       paginate_by = 20, 
                       allow_empty = True, 
                       page = pagination_id, 
                       template_name = 'core/season_list.html', 
                       extra_context = {'currentSeason': currentSeason}
                       )

def stage1(request):
    
    if request.method == 'GET':
        return render_to_response('core/season/stage1.html', {'user': request.user})
    
    elif request.method == 'POST':
        # change season status
        currentSeason = Season.objects.get(isCurrentSeason = True)
        currentSeason.seasonStatus = SeasonStatus.objects.get(name = "Scheduling Seeding Games")
        currentSeason.save()
        return render_to_response('core/season/stage1_done.html', {'user': request.user})

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
        # change season status
        currentSeason = Season.objects.get(isCurrentSeason = True)
        currentSeason.seasonStatus = SeasonStatus.objects.get(name = "Scheduling Season Games")
        currentSeason.save()
        return render_to_response('core/season/stage3_done.html', {'user': request.user})

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

