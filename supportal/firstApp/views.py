from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout
from .models import Issue, baseUser, Developer
from .forms import IssueForm, UserForm
from django.core import mail
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import datetime
import requests
import json
import time
# Create your views here.

bucket_url = 'https://api.bitbucket.org/1.0/repositories/shawdl/supportal2016test/issues'
slack_url = 'https://hooks.slack.com/services/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'
client_id = 'djnug2AYYSwzudDYdj'
client_secret = 'K42BdNv8WXAD5erXt8ZK9SEycH39mQ5u'
redirect_uri = 'https://localhost/supportal'
auth_uri = "https://bitbucket.org/site/oauth2/authorize"
token_uri = "https://bitbucket.org/site/oauth2/access_token"

#Login page, uses index.html as template
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
			g = Group.objects.get(name='Users')
			new_user = User.objects.create_user(**form.cleaned_data)
			g.user_set.add(new_user)
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
	args = {}

	if request.method == 'POST':
		form = UpdateProfile(request.POST, instance=request.user)
		form.actual_user = request.user
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('update_profile_success'))
	else:
		form = UpdateProfile()

	args['form'] = form
	return render(request, 'edit_profile.html', args)

#Main page that is currently used as a list of a all issues in the database
@login_required
def mainPage(request):
	queryset = Issue.objects.all()
	#queryset = Developer.objects.all()

	context = {
		"Issue_list": queryset,
		"title": "Main"
	}
	return render(request, "index.html", context)

#View issues, currently gets all issues from a singular repository and displays as plaintext
@login_required
def viewIssues(request):
	#lists for issue titles and content
	bucket_titles = []
	bucket_content = []
	#call api to get initial repository and find number of issues in said repository
	r = requests.get('https://api.bitbucket.org/1.0/repositories/shawdl/supportal2016test/issues/')
	bucket_json = r.json()
	issue_count = bucket_json['count']

	x = 1
	while x <= issue_count:
		#get each individual issue by id
		r2 = requests.get('https://api.bitbucket.org/1.0/repositories/shawdl/supportal2016test/issues/' + str(x))
		bucket_issues = r2.json()
		#store converted issue titles and content in the appropriate lists
		bucket_titles.append(bucket_issues['title'])
		bucket_content.append(bucket_issues['content'])
		x += 1

	#pass the lists to the template
	context = {
		"issue_title": bucket_titles,
		"issue_content": bucket_content,
		"title": "View Issues",
	}
	return render(request, "view_issues.html", context)

#Create issue form page to create an issue, currently does not actually create issues
#Issues are not sent to BitBucket, problem with authentication
@login_required
def createIssue(request):
	#retrieve client info for BitBucket auth

	#BackendApplicationClient method
	#client = BackendApplicationClient(client_id=client_id)
	#oauth = OAuth2Session(client=client)
	#token = oauth.fetch_token(token_url=token_uri, client_id=client_id, client_secret=client_secret)

	#WebApplicationClient method
	# bitbucket = OAuth2Session(client_id)
	# auth_url = bitbucket.authorization_url(auth_uri)

	if request.method == "POST":
		getUser = request.user
		form = IssueForm(request.POST)
		# form.authorization = auth_url

		if form.is_valid():
			priority = "minor"
			issue = Issue(**form.cleaned_data)
			title = form.cleaned_data['title']
			kind = form.cleaned_data['kind']
			content = form.cleaned_data['description']
			#authorization = form.cleaned_data['authorization']

			if issue.highPriority:
				current_time = datetime.datetime.now().time()
				users = Developer.objects.all()
				priority = "major"
				assigned = "unassigned"
				for user in users:
					if user.oncall_clockin <= current_time <= user.oncall_clockout:
						assigned = str(user.user)
					elif user.oncall_clockin > user.oncall_clockout:
						end = datetime.time(hour=23, minute=59, second=59, microsecond=999999)
						if user.oncall_clockin <= current_time <= end:
							assigned = str(user.user)
						elif current_time <= end:
							assigned = str(user.user)
						
				slack_payload={
					"text": str(getUser) + " just created a high priority issue:\n" + "*" + title + "*" + "\n" + ">"
					+ content + "\nAssigned to: @" + assigned
				}

				r = requests.post(slack_url, json=slack_payload)

			#JSON payload to send to bitbucket with issue
			payload = {
				"priority": priority,
				"title": title,
				"kind": kind,
				"content": content,
				"created_on": issue.timestamp,
				"reported_by":{
					"username": str(getUser),
				}
			}

			# Try to fetch token, however state changes when form is submitted
			# bitbucket.fetch_token(
			# 	token_uri,
			# 	authorization_response=authorization,
			# 	client_id=client_id,
			# 	client_secret=client_secret)

			# r = bitbucket.post(bucket_url, json=payload)

			return HttpResponseRedirect("/supportal/main")
	else:
		form = IssueForm()

	context = {
			"form": form,
			#"authUrl": r,
		}

	return render(request, "issue_form.html", context)

#Delete issues is empty, to be used to close / delete issues
@login_required
def deleteIssues(request):
	return HttpResponse("<h1>Delete Issues</h1>")