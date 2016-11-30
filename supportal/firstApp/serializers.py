from rest_framework import serializers
from django.contrib.auth.models import User
from models import baseUser

#class baseUserSerializer(serializers.ModelSerializer):
#	class Meta:
#		model = baseUser
#		field = ('user', 'time_available')