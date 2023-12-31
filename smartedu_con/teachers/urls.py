from django.urls import path
from . views import TeachersListView, TeacherDetailView
from . import views


urlpatterns = [
    path('', TeachersListView.as_view(), name='teachers'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='teacher_detail'), 
    path('teacher/edit-teacher-detail/',views.edit_teacher_detail , name='edit_teacher_detail'), 
]