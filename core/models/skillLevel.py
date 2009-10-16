from django.db import models
from nihlapp.core.models import *

class SkillLevel(models.Model):
    name = models.CharField("Skill Level Name", max_length = 30, unique = True)
    weight = models.PositiveSmallIntegerField("Weight", unique = True)

    class Meta:
		app_label = "core"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('skilllevels', 'detail', self.pk)