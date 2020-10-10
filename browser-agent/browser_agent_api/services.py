from .models import Inform
from .models import Register
import requests, dateutil.tz
from django.conf import settings
from datetime import datetime



def read_data_by_key(key_value, domain_value):
	value= Register.objects.filter(Key=key_value).filter(DomainName=domain_value)
	return value



def register_save_object(data):
	save_object= Register(**data)
	save_object.save()
	return save_object

def inform_save_object(data):
	save_object= Inform(**data)
	save_object.save()
	key_data= read_data_by_key(data['Key'], data['DomainName'])
	if len(key_data) > 0:
		URL = get_push_url()
		requests.post(url = URL, params = data) 

	return save_object	

def clean_up(domain_name, key_value=None):
	if key_value == None:
		Inform.objects.filter(DomainName= domain_name).delete()
		Register.objects.filter(DomainName= domain_name).delete()

	else:
		Inform.objects.filter(Key=key_value).filter(DomainName=domain_name).delete()
		Register.objects.filter(Key=key_value).filter(DomainName=domain_name).delete()

def clean_up_cycle():
	registered_devices = list(register_read_data().values())
	for registered_device in registered_devices:
		created_date = registered_device['created_date']
		now = datetime.now(dateutil.tz.tzutc())
		if((now - created_date).total_seconds() > settings.CLEAN_UP_SCHED):
			clean_up(registered_device['DomainName'], registered_device['Key'])
			registered_device['CLEAN_UP']=True
			requests.post(url = get_push_url(), params = registered_device)


def get_push_url():
	return settings.NODE_BASE_INTERNAL_API + "push"	


def inform_read_data():
	data= Inform.objects.all()
	return data

def register_read_data(domain_name=None, key_value=None):
	if(domain_name is None or key_value is None):
		data= Register.objects.all()
		return data
	else:
		data= Register.objects.filter(Key=key_value).filter(DomainName=domain_name)
		return data	

