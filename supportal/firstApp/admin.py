from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Issue, Developer, baseUser

class issueAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "timestamp", "createdBy", "highPriority"]

	class Meta: 
		model = Issue

class userInLine(admin.StackedInline):
	model = baseUser
	verbose_name_plural = 'User time available'

class developerInLine(admin.StackedInline):
	model = Developer
	verbose_name_plural = 'Developer oncall'

class UserAdmin(BaseUserAdmin):
	inlines = (developerInLine, userInLine)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Issue, issueAdmin)