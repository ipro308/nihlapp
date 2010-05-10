# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.contrib.localflavor.us.forms import *
#from nihlapp.core.models import *

class Club(models.Model):
    name = models.CharField("Club Name", max_length = 50, unique = True)
    #contact = models.ForeignKey(UserProfile, verbose_name = "Contact")
    contactName = models.CharField("Contact Name", max_length = 50, blank = True)
    contactEmail = models.EmailField("Contact Email", blank = True)
    contactPhone = models.CharField("Contact Phone", max_length = 15, blank = True)
    address = models.CharField("Address", max_length = 30, blank = True)
    city = models.CharField("City", max_length = 30, blank = True)
    state = models.CharField("State", max_length = 2, blank = True)
    zip = models.CharField("Zipcode", max_length = 5, blank = True)

    class Meta:
        app_label = "core"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('clubs', 'detail', self.pk)

class CreateClubForm(forms.Form):
	name = forms.CharField(label="Name")
	address = forms.CharField(label="Address")
	city = forms.CharField(label="City")
	state = USStateField(label="State",widget=USStateSelect)
	zip = USZipCodeField()
	contactName = forms.CharField(label="Contact Name")
	contactEmail = forms.EmailField(label="Contact Email")
	contactPhone = forms.CharField(label="Contact Phone")
	
	def save(self):
		new_club= Club(
		name = self.cleaned_data['name'],
		address = self.cleaned_data['address'],
		city = self.cleaned_data['city'],
		state = self.cleaned_data['state'],
		zip = self.cleaned_data['zip'],
		contactName = self.cleaned_data['contactName'],
		contactEmail = self.cleaned_data['contactEmail'],
		contactPhone = self.cleaned_data['contactPhone'],
		)
		new_club.save()
		return new_club
		