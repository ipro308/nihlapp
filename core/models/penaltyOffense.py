from django.db import models
#from nihlapp.core.models import *

class PenaltyOffense(models.Model):
    name = models.CharField("Penalty Offense", max_length = 30)
    
    class Meta:
        app_label = "core"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('penaltyoffenses', 'detail', self.pk)