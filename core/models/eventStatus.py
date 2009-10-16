from django.db import models
from nihlapp.core.models import *

class EventStatus(models.Model):
	name = models.CharField("Event Status", max_length = 30, unique = True)
    
	class Meta:
		app_label = "core"
