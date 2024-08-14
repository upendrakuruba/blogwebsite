from django.db import models
from datetime import datetime
# Create your models here.

class Contactm(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    contacted_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.email
    