from django import forms
from . models import Course, Category, Tag

class AddCourseForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Course Name'
    }))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        # 'placeholder': 'Category (Web Design, Programming, Web Development)'
    }))
    
   
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.SelectMultiple(attrs={
        'class': 'form-control',
        # 'placeholder': 'Tags (Premium, Front End, Back End)'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Description'
    }))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class':'form-control', 
        }),
        required=False
    )

    class Meta:
        model = Course
        fields = ['name','category','tags','description','image']
