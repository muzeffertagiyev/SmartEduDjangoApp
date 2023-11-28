from django.shortcuts import render,redirect
from django.contrib import messages

from django.contrib.auth.models import User
from courses.models import Course

# Create your views here.
def enroll_the_course(request):

    course_id = request.POST['course_id']
    user_id = request.POST['user_id']
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=user_id)

    if hasattr(user, 'student'):
        course.students.add(user)
        messages.info(request,f'You enrolled to the "{course.name}" course')
        return redirect('dashboard',username=user.username)
    else:
        messages.info(request,f'You should have a student account for enrolling to a course')

def release_the_course(request):
    course = Course.objects.get(id=request.POST['course_id'])
    user = User.objects.get(id=request.POST['user_id'])
    
    if hasattr(user, 'student'):
        course.students.remove(user)
        messages.info(request,f'You released "{course.name}" course')
        return redirect('dashboard',username=user.username)
    else:
        messages.info(request,f'You should have a student account for releasing to a course')