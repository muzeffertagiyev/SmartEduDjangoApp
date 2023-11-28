from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=50,blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='courses/%Y/%m/%d/',default='courses/default_course_image.png')
    facebook = models.URLField(max_length=100,blank=True)
    twitter = models.URLField(max_length=100,blank=True)
    linkedin = models.URLField(max_length=100,blank=True)
    youtube = models.URLField(max_length=100,blank=True)
    account_create_date = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
