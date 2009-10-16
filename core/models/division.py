from django.db import models
#from nihlapp.core.models import *

class Division(models.Model):
    name = models.CharField("Division Name", max_length = 30, unique = True)
    #num_teams = models.IntegerField("Number of Teams")
    #contact = models.ForeignKey(UserProfile, "Contact")
    contactName = models.CharField("Contact Name", max_length = 30, blank = True)
    contactEmail = models.EmailField("Contact Email", blank = True)

    class Meta:
		app_label = "core"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('divisions', 'detail', self.pk)
