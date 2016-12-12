from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

class Issue(models.Model):
	kinds = (('bug', 'Bug',), ('enhancement', 'Enhancement',), ('proposal', 'Proposal',), ('task', 'Task',),)

	title = models.CharField(max_length = 120, help_text="Give a title for your issue.")
	description = models.TextField(help_text="Give a description of your issue.")
	update = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	createdBy = models.ForeignKey(User)
	highPriority = models.BooleanField(default=False)
	kind = models.CharField(help_text="What kind of issue is this?", max_length=25, choices=kinds, default='bug')

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

class baseUser(models.Model):

	user = models.OneToOneField(User)
	time_available = models.DecimalField(max_digits=4, decimal_places=1, default=8)

class OnCallRotation(models.Model):

	username = models.ForeignKey(User)
	oncall_clockin = models.TimeField(auto_now_add=False)
	oncall_clockout = models.TimeField(auto_now_add=False)

	def __unicode__(self):
		return self.username