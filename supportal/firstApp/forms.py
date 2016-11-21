from django import forms
from django.contrib.auth.models import User
from .models import Issue
from django.contrib.auth import models as auth_models

class IssueForm(forms.ModelForm):

	kind = forms.ChoiceField(widget=forms.Select, choices=Issue.kinds,)

	class Meta:
		model = Issue
		fields = [
			"title",
			"kind",
			"description",
			"highPriority",
			"authorization",
		]

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			"username",
			"first_name",
			"last_name",
			"email",
			"password",
		]
