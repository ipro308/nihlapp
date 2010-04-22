from django.http import Http404
from django.views.generic import list_detail
from nihlapp.core.models import Rink
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

def confirm(request, object_id):
				return render_to_response('core/rink/confirm.html', {'object_id': object_id})
