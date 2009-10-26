from django.db import models
#from nihlapp.core.models import *

class EventType(models.Model):
    name = models.CharField("Event Type Name", max_length = 30, unique = True)

    class Meta:
		app_label = "core"
        
    def __str__(self):
        return self.name