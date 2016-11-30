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

class updateUserForm(forms.ModelForm):

	first_name = forms.CharField(label="First Name:", required=True, max_length=30)
	last_name = forms.CharField(label="Last Name:", required=True, max_length=30)
	email = forms.EmailField(label="Email:", required=True)

	class Meta:
		model = User
		fields = [
			"first_name",
			"last_name",
			"email"
		]

class deleteForm(forms.Form):
	id_to_be_deleted = forms.IntegerField(label="ID of issue to delete:")		
