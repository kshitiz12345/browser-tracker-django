from rest_framework import serializers
from .models import Inform
from .models import Register


class InformSerializer(serializers.Serializer):
	key= serializers.CharField(max_length=20)
	response= serializers.CharField(max_length=200)


class RegisterSerializer(serializers.Serializer):
	key= serializers.CharField(max_length=20)
	#response= serializers.CharField(max_length=200)
