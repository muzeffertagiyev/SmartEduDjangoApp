from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from . forms import LoginForm, RegisterForm

from courses.models import Course


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # we use cleaned data because in login form we have used basic form. we will not use this method in register
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                   
                    messages.info(request,'Disabled Account')
            else:
                messages.info(request,'Check Your Username and Password')
    else:
        form = LoginForm()

    return render(request,'login.html',{'form':form})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email already exists in the database
            if User.objects.filter(email=email).exists():
                messages.info(request,'This email is already in use. Please choose a different one or login instead.')
                return render(request, 'register.html',{'form':form})
            
            form.save()
            messages.success(request, 'Account has been created, You can Login')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request,'register.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def user_dashboard(request,username):
    current_user = User.objects.get(username=username)
    # joined_courses comes from the courses models 
    courses = current_user.joined_courses.all()
    
    context = {
        "courses":courses,
        "user": current_user
    }
    
    return render(request, 'dashboard.html',context)



def enroll_the_course(request):
    course_id = request.POST['course_id']
    user_id = request.POST['user_id']
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=user_id)
    course.students.add(user)

    return redirect('dashboard',user.username)

def release_the_course(request):
    course = Course.objects.get(id=request.POST['course_id'])
    user = User.objects.get(id=request.POST['user_id'])
    course.students.remove(user)

    return redirect('dashboard',user.username)