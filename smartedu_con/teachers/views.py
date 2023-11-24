from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . models import Teacher
from courses.models import Course

class TeachersListView(ListView):
    model = Teacher
    template_name = 'teachers.html'
    context_object_name = 'teachers'
    # queryset = Teacher.objects.all()[:1]
    # paginate_by = 2
    # we can use pagination too , for the html code for changing the pages look at the documentation

    # we can find this virables from documentation and work on them as we want, we can use some function instead


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teacher_detail.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(available=True,teacher=self.kwargs['pk'])
        return context

