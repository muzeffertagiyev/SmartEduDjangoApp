from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . models import Teacher
from courses.models import Course

from . forms import EditTeacherDetailForm



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
    
@login_required(login_url='login')
def edit_teacher_detail(request):
    current_user = request.user

    if hasattr(current_user, 'teacher'): 
        teacher = Teacher.objects.get(id=int(current_user.teacher.id))
        print(teacher)
        if teacher.username == current_user.username:
            if request.method == 'POST':
                # instance will add all data of the teacher into forms.
                form = EditTeacherDetailForm(request.POST, instance=teacher)
                if form.is_valid():
                    # creating not saved course form, because we will check image and add teacher
                    
                    if 'image' in request.FILES:
                        teacher.image = request.FILES['image']


                    # For saving many to many relationships data
                    teacher.save()
                    form.save()

                    messages.success(request, f"Your details were updated")
                    return redirect('dashboard', username=current_user.username)
                
                # if the error happens in the submission
                else:
                    messages.error(request, 'There was an error with the form submission')

            # if not submitted
            else:
                form = EditTeacherDetailForm(instance=teacher)

            return render(request, 'teacher_edit_detail.html', {'form': form})
        else:
            messages.info(request,f"You can only edit your details")
            return redirect('dashboard', username=current_user.username)
    else:
        messages.info(request,f"You cannot edit your details")
        return redirect('dashboard', username=current_user.username)

