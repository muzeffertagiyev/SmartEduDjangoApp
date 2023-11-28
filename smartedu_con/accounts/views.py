from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from . forms import LoginForm, RegisterForm

from students.models import Student
from teachers.models import Teacher
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
                    return redirect('dashboard',username=user.username)
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
            
            user = form.save()
            first_name=form.cleaned_data['first_name'].title()
            last_name=form.cleaned_data['last_name'].title()
            username=form.cleaned_data['username'].lower()

            user_type = form.cleaned_data.get('user_type')
            if user_type == 'student':
                Student.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    username=username
                    )
            elif user_type == 'teacher':
                Teacher.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    username=username
                    )

            messages.success(request, 'Account has been created, You can Login')
            return redirect('login')  # Change 'home' to the URL you want to redirect to after registration
    else:
        form = RegisterForm()

    return render(request,'register.html',{'form':form})

def user_logout(request):
    logout(request)
    messages.info(request,'You Logged out , now you can login again')
    return redirect('login')


@login_required(login_url='login')
def user_dashboard(request,username):
    current_user = get_object_or_404(User, username=username)
    # joined_courses comes from the courses models 
    teacher = None
    if hasattr(request.user, 'teacher'):
        courses = Course.objects.filter(teacher=current_user.teacher).order_by('-date')
        teacher = Teacher.objects.get(id=current_user.teacher.id)
    else:
        courses = current_user.joined_courses.all()
    
    context = {
        "courses":courses,
        "user": current_user,
        "teacher":teacher
    }
    
    return render(request, 'dashboard.html',context)



