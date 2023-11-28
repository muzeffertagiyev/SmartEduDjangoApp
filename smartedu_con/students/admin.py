from django.contrib import admin
from . models import Student



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name')
    search_fields = ('username','first_name','last_name')