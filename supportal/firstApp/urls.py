from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from firstApp import views as firstapp_views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^main/$', firstapp_views.mainPage, name='main'),
	url(r'^$', auth_views.login, name='login'),
    url(r'^viewIssues/$', firstapp_views.viewIssues, name='viewIssues'),
    url(r'^create/$', firstapp_views.createIssue, name='createIssue'),
    url(r'^newuser/$', firstapp_views.newUser, name='newUser'),
    url(r'^updateprofile/$', firstapp_views.updateProfile, name='updateProfile'),
    url(r'^logout/$', firstapp_views.logout_view, name='logout'),
    url(r'^password/reset/$', auth_views.password_reset, {'post_reset_redirect' : '/supportal/password/reset/done/'}, name="password_reset"),
    url(r'^password/reset/done/$', auth_views.password_reset_done),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'post_reset_redirect' : '/supportal/password/done/'}, name='password_reset_confirm'),
    url(r'^password/done/$', auth_views.password_reset_complete),
    url(r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/create/$', firstapp_views.ApiCreateIssue),
    url(r'^api/delete/$', firstapp_views.ApiDeleteIssue),
]

urlpatterns = format_suffix_patterns(urlpatterns)
