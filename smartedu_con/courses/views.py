from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . models import Course, Category, Tag
from . forms import AddCourseForm


from teachers.models import Teacher



def course_list(request, category_slug=None, tag_slug=None):
    category_page = None
    tag_page = None
    categories = Category.objects.all()
    tags = Tag.objects.all()

    current_user = request.user
    enrolled_course_ids = set()

    if category_slug != None:
        category_page = get_object_or_404(Category,slug=category_slug)
        courses = Course.objects.filter(available=True,category=category_page).order_by('-date')
    elif tag_slug != None:
        tag_page = get_object_or_404(Tag,slug=tag_slug)
        courses = Course.objects.filter(available=True, tags=tag_page).order_by('-date')
    else:
        courses = Course.objects.all().order_by('-date')

        # for excluding enrolled courses
        # if current_user.is_authenticated:
        #     enrolled_courses = current_user.joined_courses.all()
        #     courses = Course.objects.all().order_by('-date')

        #     for course in enrolled_courses:
        #         courses = courses.exclude(id = course.id)

        
    if current_user.is_authenticated: 
        # Get the courses that the user has already enrolled in
        enrolled_courses = current_user.joined_courses.all()

        # Create a set of course IDs that the user has enrolled in
        enrolled_course_ids = set(course.id for course in enrolled_courses)

    context = {
        'courses':courses,
        'categories':categories,
        'tags':tags,
        'enrolled_course_ids': enrolled_course_ids,
    }

    return render(request, 'courses.html', context)


def course_detail(request, category_slug, course_id):
    course = Course.objects.get(category__slug=category_slug,id=course_id)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    current_user = request.user
    enrolled_courses = set()
    if current_user.is_authenticated:
        enrolled_courses = current_user.joined_courses.all()

    context = {
        'course':course,
        'categories':categories,
        'tags':tags,
        'enrolled_courses':enrolled_courses
    }

    return render(request, 'course_detail.html',context)


def search(request):
    courses = Course.objects.filter(name__contains = request.GET['search'])
    categories = Category.objects.all()
    tags = Tag.objects.all()

    current_user = request.user
    enrolled_course_ids = set()

    if current_user.is_authenticated: 
        # Get the courses that the user has already enrolled in
        enrolled_courses = current_user.joined_courses.all()

        # Create a set of course IDs that the user has enrolled in
        enrolled_course_ids = set(course.id for course in enrolled_courses)

    context = {
        'courses':courses,
        'categories':categories,
        'tags':tags,
        'enrolled_course_ids': enrolled_course_ids
    }

    return render(request, 'courses.html', context)


def add_course(request):
    current_user = request.user
    is_add_course_page = True
    if current_user.is_authenticated:
        if hasattr(current_user, 'teacher'):
            teacher = Teacher.objects.get(user=current_user)
        
            if request.method == 'POST':
                form = AddCourseForm(request.POST)

                if form.is_valid():
                    course_name = form.cleaned_data['name']
                    # Save the form data to the database
                    course = form.save(commit=False)
                    if 'image' in request.FILES:
                        course.image = request.FILES['image']
                    
                    # Set the teacher before saving the course
                    course.teacher = teacher
                    course.save()

                    # For saving many to many relationships data
                    form.save_m2m()

                    messages.info(request,f'Course "{course_name}" was added successfully')

                    return redirect('courses')
                else:
                    messages.info(request,'There was an error with the form submission')
                    return redirect('add_course')    
            else:
                form = AddCourseForm(initial={'teacher': teacher})

            return render(request,'add_course.html',{'form':form,'is_add_course_page': is_add_course_page})
        else:
            # Redirect to the user's dashboard with a message if the user is not teacher
            messages.info(request, 'You do not have permission to add a course.Only Teachers can')
            return redirect('dashboard',username=current_user
                    .username)
    else:
        # Redirect to the login page if the user is not authenticated
        return redirect('login')  
    
@login_required(login_url='login')
def edit_course(request,category_slug,course_id):
    current_user = request.user
    course = Course.objects.get(id=course_id,category__slug=category_slug)

    if hasattr(current_user, 'teacher'): 
        teacher = Teacher.objects.get(user=current_user)
        if course.teacher.username == current_user.username:
            if request.method == 'POST':
                # instance will add all data of the course into forms.
                form = AddCourseForm(request.POST, instance=course)
                if form.is_valid():
                    # creating not saved course form, because we will check image and add teacher
                    course = form.save(commit=False)

                    if 'image' in request.FILES:
                        course.image = request.FILES['image']

                    course.teacher = teacher
                    course.save()

                    # For saving many to many relationships data
                    form.save_m2m()
                    form.save()

                    messages.success(request, f"Course '{course.name}' was edited successfully")
                    return redirect('dashboard', username=current_user.username)
                
                # if the error happens in the submission
                else:
                    messages.error(request, 'There was an error with the form submission')

            # if not submitted
            else:
                form = AddCourseForm(instance=course,initial={'teacher': teacher})

            return render(request, 'add_course.html', {'form': form})
        else:
            messages.info(request,f"You can only edit your courses")
            return redirect('dashboard', username=current_user.username)
    else:
        messages.info(request,f"You cannot edit a course")
        return redirect('dashboard', username=current_user.username)
    
@login_required(login_url='login')
def delete_course(request,category_slug, course_id):
    current_user = request.user
    
    if hasattr(current_user, 'teacher'):
        course = Course.objects.get(id=course_id,category__slug=category_slug)
        if course.teacher.username == current_user.username:
            messages.info(request,f"Course '{course.name}' was deleted successfully")
            course.delete()
            return redirect('dashboard', username=current_user.username)
        else:
            messages.info(request,f"You can only delete your courses")
            return redirect('dashboard', username=current_user.username)
    else:
        messages.info(request,f"You cannot delete a course")
        return redirect('dashboard', username=current_user.username)
    
    
        


    




#  for checking the errors in the form.
# else:
#     default_data = {'teacher': default_teacher}
#     messages.error(request,'There was an error with the form submission')
#     # You can iterate over the form errors and add them to the messages
#     for field, errors in form.errors.items():
#         for error in errors:
#             messages.error(request, f"{field.capitalize()}: {error}")
    
#     return redirect('add_course') 


# def course_list(request):
#     courses = Course.objects.all().order_by('-date')
#     categories = Category.objects.all()
#     tags = Tag.objects.all()

#     context = {
#         'courses':courses,
#         'categories':categories,
#         'tags':tags
#     }

#     return render(request, 'courses.html', context)



# def category_list(request, category_slug):
#     courses = Course.objects.all().filter(category__slug=category_slug)
#     categories = Category.objects.all()
#     tags = Tag.objects.all()

#     context = {
#         'courses':courses,
#         'categories':categories,
#         'tags':tags
#     }


#     return render(request, 'courses.html',context)

# def tag_list(request, tag_slug):
#     courses = Course.objects.all().filter(tags__slug=tag_slug)
#     categories = Category.objects.all()
#     tags = Tag.objects.all()

#     context = {
#         'courses':courses,
#         'categories':categories,
#         'tags':tags
#     }


#     return render(request, 'courses.html',context)