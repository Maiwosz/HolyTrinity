from django.db import models

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    date = models.DateTimeField('event date')

    def __str__(self):
        return self.title
