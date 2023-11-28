from django.urls import path
from . import views


urlpatterns = [
    path('', views.course_list, name='courses'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<slug:category_slug>/<int:course_id>', views.edit_course, name='edit_course'),
    path('delete-course/<slug:category_slug>/<int:course_id>', views.delete_course, name='delete_course'),
    path('<slug:category_slug>/<int:course_id>', views.course_detail, name='course_detail'),
    path('categories/<slug:category_slug>', views.course_list, name='courses_by_category'),
    path('tags/<slug:tag_slug>', views.course_list, name='courses_by_tag'),
    path('search/', views.search, name='search'),
    
]
