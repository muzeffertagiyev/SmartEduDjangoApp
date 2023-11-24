from django.db import models
from teachers.models import Teacher
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    # if we delete a teacher then their courses will be deleted to 
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag,blank=True,null=True)
    students = models.ManyToManyField(User,blank=True,related_name='joined_courses')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='courses/%Y/%m/%d/', default='courses/default_course_image.png')
    date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    

    # in admin page after creation of the course then it will be shown by its name
    def __str__(self):
        return self.name