from django.db import models
from nihlapp.core.models import *

class Parameter(models.Model):
    name = models.CharField("Event Type Name", max_length = 30, unique = True)
    value = models.CharField("Event Type Name", max_length = 30)

    class Meta:
		app_label = "core"