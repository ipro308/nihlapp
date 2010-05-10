from django.db import models
#from nihlapp.core.models import *

class EventStatus(models.Model):
	name = models.CharField("Event Status", max_length = 50, unique = True)
    
	class Meta:
		app_label = "core"

	def __str__(self):
		return self.name