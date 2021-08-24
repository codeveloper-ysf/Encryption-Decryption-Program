from django.db import models

# Create your models here.
class Method(models.Model):
	name = models.CharField(max_length=200, blank=True, null=True)
	explanation = models.TextField(blank=True, null=True)
	image = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name