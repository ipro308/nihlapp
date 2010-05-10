# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import list_detail
from nihlapp.core.models import Rink
from nihlapp.core.models.rink import CreateRinkForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

def create(request):
	if request.method == 'POST': # If the form has been submitted...
		form = CreateRinkForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			print "form is valid"
			print form
			new_rink = form.save()
			return HttpResponseRedirect('/rinks/confirm/create/%d' % new_rink.id)
			print "form is not valid"
	form = CreateRinkForm() # An unbound form
	return render_to_response('core/rink_form.html', {
				'form': form, 'user': request.user
				})

def confirm(request, object_id):
				return render_to_response('core/rink/confirm.html', {'object_id': object_id})
