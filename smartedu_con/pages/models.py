from django.db import models
from django.utils import timezone


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        local_time = timezone.localtime(self.date)
        return f"Email from : {self.email} Date: {local_time.strftime('%Y-%m-%d / %H:%M:%S')}"