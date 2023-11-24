from django.shortcuts import render,get_object_or_404

from . models import Course, Category, Tag



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