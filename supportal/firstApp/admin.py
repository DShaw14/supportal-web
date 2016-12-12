from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Issue, baseUser, OnCallRotation

class issueAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "timestamp", "createdBy", "highPriority"]

	class Meta: 
		model = Issue

class userInLine(admin.StackedInline):
	model = baseUser
	verbose_name_plural = 'User time available'

class OnCallAdmin(admin.ModelAdmin):
	list_display = ["username", "oncall_clockin", "oncall_clockout"]

	class Meta:
		model = OnCallRotation

class UserAdmin(BaseUserAdmin):
	inlines = (userInLine, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Issue, issueAdmin)
admin.site.register(OnCallRotation, OnCallAdmin)