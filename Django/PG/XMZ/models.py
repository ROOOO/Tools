from __future__ import unicode_literals

from django.db import models

# Create your models here.
class XMZ_URTracker(models.Model):
	url = models.CharField(max_length = 50)
	state = models.CharField(max_length = 20)
	revision = models.CharField(max_length = 10)
	task = models.TextField()

class XMZ_SVNLog(models.Model):
	revision = models.IntegerField()
	author = models.CharField(max_length = 20)
	log = models.TextField()
