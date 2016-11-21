from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from firstApp import views as firstapp_views

urlpatterns = [
	url(r'^main/$', firstapp_views.mainPage, name='main'),
	url(r'^$', auth_views.login, name='login'),
    url(r'^viewIssues/$', firstapp_views.viewIssues, name='viewIssues'),
    url(r'^create/$', firstapp_views.createIssue, name='createIssue'),
    url(r'^delete/$', firstapp_views.deleteIssues, name='viewIssues'),
    url(r'^newuser/$', firstapp_views.newUser, name='newUser'),
    url(r'^updateprofile/$', firstapp_views.updateProfile, name='updateProfile'),
    url(r'^logout/$', firstapp_views.logout_view, name='logout'),
    url(r'^password/reset/$', auth_views.password_reset, {'post_reset_redirect' : '/password/reset/done/'}, name="password_reset"),
    url(r'^password/reset/done/$', auth_views.password_reset_done),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'post_reset_redirect' : '/password/done/'}),
    url(r'^password/done/$', auth_views.password_reset_complete),
]
