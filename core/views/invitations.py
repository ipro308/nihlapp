from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nihlapp.core.models import Invitation, InvitationForm, Team
from django.db.models import Q
#from datetime import datetime, timedelta

def invitation(request):
    pass

