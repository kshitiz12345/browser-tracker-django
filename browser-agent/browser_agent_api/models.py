from django.db import models
from django.utils.timezone import now

# Alert models.
class Inform(models.Model):
	Key= models.CharField(max_length=20)
	Response= models.CharField(max_length=200)
	DomainName= models.CharField(max_length=200)
	Type= models.IntegerField()
	created_date = models.DateTimeField(default=now, editable=False)
	"""docstring for ClassName"""

#Collect Model

class Register(models.Model):
	Key= models.CharField(max_length=20)
	DomainName= models.CharField(max_length=200)
	created_date = models.DateTimeField(default=now, editable=False)

	#response= models.CharField(max_length=200)
