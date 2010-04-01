# -*- coding: utf-8 -*-
from django.db import models
from nihlapp.core.models import Season, Division, Club, SkillLevel
from django import forms

class Team(models.Model):
	name = models.CharField("Team Name", max_length = 50)
	season = models.ForeignKey(Season, verbose_name = "Season")
	division = models.ForeignKey(Division, verbose_name = "Division")
	club = models.ForeignKey(Club, verbose_name = "Club")
	skillLevel = models.ForeignKey(SkillLevel, verbose_name = "Skill Level")
	#manager = models.ForeignKey(UserProfile, verbose_name = "Manager")
	#coach = models.ForeignKey(UserProfile, verbose_name = "Coach")
	managerName = models.CharField("Manager Name", max_length = 50)
	managerEmail = models.EmailField("Manager Email")
	managerPhone = models.CharField("Manager Phone", max_length = 15, blank = True)
	coachName = models.CharField("Coach Name", max_length = 50, blank = True)
	coachEmail = models.EmailField("Coach Email", blank = True)
	coachPhone = models.CharField("Coach Phone", max_length = 15, blank = True)

	class Meta:
		app_label = "core"

	def __str__(self):
		return "[%s %s] %s" % (self.division.name, self.skillLevel.name, self.name)

	def get_absolute_url(self):
		return "/%s/%s/%s" % ('teams', 'detail', self.pk)

class CreateTeamForm(forms.Form):
	
	name = forms.CharField(label="Team Name",max_length=50)
	season = forms.ModelChoiceField(label="Season", queryset=Season.objects.all().order_by('year'))
	division = forms.ModelChoiceField(label="Division", queryset=Division.objects.all().order_by('name'), initial=Division.objects.filter(pk=1))
	club = forms.ModelChoiceField(label="Club", queryset=Club.objects.all().order_by('name'),initial=Club.objects.filter(pk=1))
	skillLevel = forms.ModelChoiceField(label="Skill Level", queryset=SkillLevel.objects.all().order_by('name'), initial=SkillLevel.objects.filter(pk=1))
	managerName = forms.CharField(label="Manager Name",max_length=50)
	managerEmail = forms.EmailField(label="Manager Email")
	managerPhone = forms.CharField(label="Manager Phone",max_length=15)
	coachName = forms.CharField(label="Coach Name",max_length=50)
	coachEmail = forms.EmailField(label="Coach Email")
	coachPhone = forms.CharField(label="Coach Phone",max_length=15)
	def __init__(self, *args, **kwargs):
		super(CreateTeamForm, self).__init__(*args, **kwargs)
		self.base_fields['season'].initial = Season.objects.filter(pk=1)

	def save(self):
		new_team = Team.objects.create_team(
			name = self.cleaned_data['name'],
			season = self.cleaned_data['season'],
			division = self.cleaned_data['division'],
			club = self.cleaned_data['club'],
			skilllevel = self.cleaned_data['skilllevel'],
			managerName = self.cleaned_data['managerName'],
			manageEmail = self.cleaned_data['manageEmail'],
			managerPhone = self.cleaned_data['managerPhone'],
			coachName = self.cleaned_data['coachName'],
			coachEmail = self.cleaned_data['coachEmail'],
			coachPhone = self.cleaned_data['coachPhoe'],
			)
		new_team.save()
		return new_team