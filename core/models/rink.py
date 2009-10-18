from django.db import models
from nihlapp.core.models import *

class Rink(models.Model):
    name = models.CharField("Rink Name", max_length = 30, unique = True)
    address = models.CharField("Address", max_length = 30, blank = True)
    city = models.CharField("City", max_length = 30, blank = True)
    state = models.CharField("State", max_length = 2, blank = True)
    zip = models.CharField("Zipcode", max_length = 5, blank = True)
    contactName = models.CharField("Contact Name", max_length = 30, blank = True)
    contactEmail = models.EmailField("Contact Name", max_length = 30, blank = True)
    contactPhone = models.CharField("Contact Phone Number", max_length = 15, blank = True)
    
    class Meta:
        app_label = "core"
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/%s/%s/%s" % ('rinks', 'detail', self.pk)