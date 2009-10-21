from django.db import models
from nihlapp.core.models import *

class Parameter(models.Model):
    name = models.CharField("Event Type Name", max_length = 30, unique = True)
    value = models.CharField("Event Type Name", max_length = 30)

    class Meta:
		app_label = "core"
        
    def __str__(self):
        return self.value        
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('parameters', 'detail', self.pk)    