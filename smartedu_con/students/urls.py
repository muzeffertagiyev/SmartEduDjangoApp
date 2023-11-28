from django.urls import path
from . import views


urlpatterns = [
    path('enroll_the_course/',views.enroll_the_course, name='enroll_the_course'),
    path('release_the_course/',views.release_the_course, name='release_the_course')
]