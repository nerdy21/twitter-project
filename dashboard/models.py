from django.db import models

# Create your models here.

class SearchLog(models.Model):
	search_query = models.CharField(max_length=20)
	time = models.DateTimeField()