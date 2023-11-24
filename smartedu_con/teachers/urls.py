from django.urls import path
from teachers.views import TeachersListView, TeacherDetailView


urlpatterns = [
    path('', TeachersListView.as_view(), name='teachers'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='teacher_detail'), 
]