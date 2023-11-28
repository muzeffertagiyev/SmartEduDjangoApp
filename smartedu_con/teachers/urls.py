from django.urls import path
from . views import TeachersListView, TeacherDetailView


urlpatterns = [
    path('', TeachersListView.as_view(), name='teachers'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='teacher_detail'), 
]