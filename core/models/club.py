from django.db import models
from nihlapp.core.models import *

class Club(models.Model):
    name = models.CharField("Club Name", max_length = 30, unique = True)
    #contact = models.ForeignKey(UserProfile, verbose_name = "Contact")
    contactName = models.CharField("Contact Name", max_length = 30, blank = True)
    contactEmail = models.EmailField("Contact Email", blank = True)
    address = models.CharField("Address", max_length = 30, blank = True)
    city = models.CharField("City", max_length = 30, blank = True)
    state = models.CharField("State", max_length = 2, blank = True)
    zip = models.CharField("Zipcode", max_length = 5, blank = True)

    class Meta:
	    app_label = "core"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('clubs', 'detail', self.pk)
