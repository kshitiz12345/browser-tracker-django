from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .services import inform_save_object
from .services import register_save_object
from .health_check import health_check
from .services import clean_up
from django.conf import settings
from django.core import serializers
from .models import Inform
from .models import Register
from .serializers import InformSerializer
from django.views.decorators.csrf import csrf_exempt
from .services import inform_read_data
from .services import register_read_data


# Create your views here.

@csrf_exempt
def inform(request):
	if 'Token' not in request.headers or request.headers['Token'] != settings.SECRET_KEY:
		return JsonResponse("", safe=False, status=401)

	if request.method == 'GET':
		inform_data = inform_read_data()
		return JsonResponse(list(inform_data.values()), safe=False, status=200)

	if request.method == 'POST':
		data= JSONParser().parse(request)
		health_check(data)	

		if data['Type'] == 0:
			new_value = inform_save_object(data)	
		elif data['Type'] == 2:
			clean_up(data['DomainName'])
		return JsonResponse("", safe=False, status=200)

@csrf_exempt
def register(request):
	if request.method == 'POST':
		data= JSONParser().parse(request)
		new_value= register_save_object(data)
		return JsonResponse("", safe=False, status=200)

	if request.method == 'DELETE':
		clean_up(data['DomainName'], data['Key'])
		return JsonResponse("", safe=False, status=200)


	if request.method == 'GET':
		register_data = register_read_data(request.GET.get('DomainName'), request.GET.get('Key'))
		devices = list(register_data.values())
		return JsonResponse(devices, safe=False, status=200)






