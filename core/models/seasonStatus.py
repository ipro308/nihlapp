from django.db import models
from nihlapp.core.models import *

class SeasonStatus(models.Model):
	name = models.CharField("Season Status", max_length = 20, blank = False, unique = True)
	
	class Meta:
		app_label = "core"
	
	def __str__(self):
		return self.status
