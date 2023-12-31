from django.contrib import admin
from . models import Teacher



@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name')
    search_fields = ('username','first_name','last_name')