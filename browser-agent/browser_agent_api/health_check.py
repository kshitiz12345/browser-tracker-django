import sched, requests, time, threading
from django.conf import settings
from .services import get_push_url, clean_up_cycle

HEALTH_CHECK = {
	'TIGER_IS_DOWN' : False,
	'UPDATE_BROWSERS_SERVER_DOWN' : False,
	'STARTED' : False
}

# instance is created 
scheduler = sched.scheduler(time.time, 
			time.sleep) 


def health_check(data):
	if(HEALTH_CHECK['UPDATE_BROWSERS_SERVER_DOWN'] is True):
		URL = get_push_url()
		requests.post(url = URL, params = {
				'TIGER_IS_UP' : True
			})

	HEALTH_CHECK['TIGER_IS_DOWN'] = False
	HEALTH_CHECK['UPDATE_BROWSERS_SERVER_DOWN'] = False


def monitor_health():
	clean_up_cycle()
	if(HEALTH_CHECK['TIGER_IS_DOWN'] is False):
		HEALTH_CHECK['TIGER_IS_DOWN'] = True
	elif(HEALTH_CHECK['UPDATE_BROWSERS_SERVER_DOWN'] is False):
		URL = get_push_url()
		requests.post(url = URL, params = {
				'TIGER_IS_DOWN' : HEALTH_CHECK['TIGER_IS_DOWN']
			})
		HEALTH_CHECK['UPDATE_BROWSERS_SERVER_DOWN'] = True
	next_event()	
		


def next_event():
	e1 = scheduler.enter(settings.HEALTH_CHECK_SCHED, 1,  
                     monitor_health) 
	scheduler.run()	 



def start_monitoring():
	if(HEALTH_CHECK['STARTED'] is False):
		threading.Thread(target=next_event).start()
		HEALTH_CHECK['STARTED'] = True

start_monitoring()
			






	
