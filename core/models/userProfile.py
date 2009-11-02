from django.db import models
from django.contrib.auth.models import User
from nihlapp.core.models import Team, Club

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    team = models.ForeignKey(Team, verbose_name = "User's Team")
    club = models.ForeignKey(Club, verbose_name = "User's Club")
    email = models.EmailField("Email", max_length = 50)
    phone = models.CharField("Phone", max_length = 10)
    confirmation = models.CharField("Confirmation Key", max_length = 64, unique = True, blank = True, null = True)
    confirmed = models.NullBooleanField("Email Confirmed", default = False, blank = True, null = True)

    class Meta:
        app_label = "core"

    def __str__(self):
        return self.user.username

	def get_absolute_url(self):
		return "/%s/%s/%s" % ('users', 'detail', user.pk)