from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='courses/%Y/%m/%d/', default='courses/default_course_image.png')
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)


    # in admin page after creation of the course then it will be shown by its name
    def __str__(self):
        return self.name