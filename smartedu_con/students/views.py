from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from courses.models import Course

# Create your views here.
def enroll_the_course(request):
    course_id = request.POST['course_id']
    user_id = request.POST['user_id']
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=user_id)
    course.students.add(user)

    return redirect('dashboard',username=user.username)

def release_the_course(request):
    course = Course.objects.get(id=request.POST['course_id'])
    user = User.objects.get(id=request.POST['user_id'])
    course.students.remove(user)

    return redirect('dashboard',username=user.username)