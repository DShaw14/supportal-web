from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout
from .models import Issue, baseUser, OnCallRotation
from .forms import IssueForm, UserForm, updateUserForm, deleteForm
from django.core import mail
from bitbucket.bitbucket import Bitbucket
import datetime
import requests
import json
import time
import logging

bucket_url = 'https://api.bitbucket.org/1.0/repositories/shawdl/supportal2016test/issues'
slack_url = 'https://hooks.slack.com/services/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'
bbUser = 'shawdl'
bbPass = 'supportal2016'

#Login page, uses index.html as template and django built in login
def login(request):
	context = {
		"title": "Login"
	}
	return render(request, "index.html", context)

#Logout view logs out user and returns them to the login page, should implement a message if possible
def logout_view(request):
	logout(request)
	return redirect('login')

#New user page, creates a form to create new user, once new user is created redirects the user to the login page
#which the user can then immeadiately login
def newUser(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(**form.cleaned_data)
			new_user.save()

			#MUST SETUP EMAIL SERVICE TO USE
			mail.send_mail(
				'Oak Labs - Supportal: Account ' + str(new_user.username) + ' has been created',
				'Your account with Supportal has been created. Thank you.',
				'supportal@oaklabs.io',
				[str(new_user.email)],
			)
			return HttpResponseRedirect("/supportal/")
	else:
		form = UserForm()

	return render(request, "adduser.html", {"form": form})

#*****Need to fix, tries to make new user instead of updating user*****
@login_required
def updateProfile(request):
	getUser = request.user
	if not request.user.is_superuser:
		getbaseUser = baseUser.objects.get(user=getUser)
	if request.method == 'POST':
		form = updateUserForm(request.POST, instance=request.user)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			return HttpResponseRedirect("/supportal/main")
	else:
		form = updateUserForm()

	if not request.user.is_superuser:
		context = {
			"form": form,
			"current_first": getUser.first_name,
			"current_last": getUser.last_name,
			"current_email":getUser.email,
			"hours_avail": getbaseUser.time_available,
		}
	else:
		context = {
			"form": form,
			"current_first": getUser.first_name,
			"current_last": getUser.last_name,
			"current_email":getUser.email,
		}
	return render(request, 'update_profile.html', context)

#Main page
@login_required
def mainPage(request):
	context = {
		"title": "Main"
	}
	return render(request, "index.html", context)


#View issues, currently gets all issues from a singular repository and displays as a formatted table
@login_required
def viewIssues(request):
	#lists for issue titles and content
	bucket_id = []
	bucket_titles = []
	bucket_content = []
	bucket_kind = []
	bucket_priority = []
	#call api to get initial repository and find number of issues in said repository
	r = requests.get(bucket_url)
	bucket_json = r.json()
	issue_count = bucket_json['count']

	if request.method == "POST":
		form = deleteForm(request.POST)

		if form.is_valid():
			bb = Bitbucket(bbUser, bbPass, repo_name_or_slug="supportal2016test")
			success, result = bb.issue.delete(issue_id=form.cleaned_data['id_to_be_deleted'])
	else:
		form = deleteForm()

	x = 1 #issue counter
	y = x #id counter
	while x <= issue_count:
		#get each individual issue by id
		r2 = requests.get('https://api.bitbucket.org/1.0/repositories/shawdl/supportal2016test/issues/' + str(y))
		if r2.text == "Not Found":
			#y is necessary because x = count only counts the number of issues, meaning that it will not reach an id of 7
			#with a count of 3. Thus, y helps us reach the other ids
			y += 1
		else:
			bucket_issues = r2.json()
			print(r2.status_code)
			print(r2.text)
		#store converted issue titles and content in the appropriate lists, only if the issues have a status of open
			if bucket_issues['status'] != "closed":
				bucket_id.append(bucket_issues['local_id'])
				bucket_titles.append(bucket_issues['title'])
				bucket_content.append(bucket_issues['content'])
				bucket_kind.append(bucket_issues['metadata']['kind'])
				bucket_priority.append(bucket_issues['priority'])
		#Move to next issue
			x += 1
			y += 1

	zipped_data = zip(bucket_id, bucket_titles, bucket_content, bucket_kind, bucket_priority)
	#pass the lists to the template
	if request.user.is_superuser:
		context = {
			"zipped_data": zipped_data,
			"title": "View Issues",
			"bucket_url": bucket_url,
			"form": form
		}
	else:
		context = {
			"zipped_data": zipped_data,
			"title": "View Issues",
			"bucket_url": bucket_url
		}

	return render(request, "view_issues.html", context)

@login_required
def createIssue(request):
	if request.method == "POST":
		getUser = request.user
		form = IssueForm(request.POST)

		if form.is_valid():
			priority = "minor"
			issue = Issue(**form.cleaned_data)
			title = form.cleaned_data['title']
			kind = form.cleaned_data['kind']
			content = form.cleaned_data['description']

			if issue.highPriority:
				current_time = datetime.datetime.now().time()
				users = OnCallRotation.objects.all()
				priority = "major"
				assigned = "unassigned"
				for user in users:
					if user.oncall_clockin <= current_time <= user.oncall_clockout:
						assigned = str(user.username)
					elif user.oncall_clockin > user.oncall_clockout:
						end = datetime.time(hour=23, minute=59, second=59, microsecond=999999)
						if user.oncall_clockin <= current_time <= end:
							assigned = str(user.username)
						elif current_time <= end:
							assigned = str(user.username)
						
				slack_payload={
					"text": str(getUser) + " just created a high priority issue:\n" + "*" + title + "*" + "\n" + ">"
					+ content + "\nAssigned to: @" + assigned
				}

				r = requests.post(slack_url, json=slack_payload)

			bb = Bitbucket(bbUser, bbPass, repo_name_or_slug="supportal2016test")
			success, result = bb.issue.create(
				title=u''+title,
				content=u''+content,
				priority=u''+priority,
				responsible=bb.username,
				status=u'new',
				kind=u''+kind)

	else:
		form = IssueForm()

	if request.user.is_superuser:
		context = {
			"form": form,
		}

	else:
		context = {
			"form": form,
			"hours_avail": 8
		}

	return render(request, "issue_form.html", context)