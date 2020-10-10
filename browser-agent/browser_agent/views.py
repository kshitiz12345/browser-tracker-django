from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render


@csrf_exempt
def home(request):
	if request.method == 'GET':
		return render(request, 'home.html', {
				'NODE_BASE_API' : settings.BASE_API
			})