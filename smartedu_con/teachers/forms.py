from django import forms
from . models import Teacher

class EditTeacherDetailForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'First Name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Last Name'
    }))
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Title (Programmer, Web Developer)'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Description'
    }))
    facebook = forms.URLField(widget=forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'Facebook'
    }),
        required=False
        )
    twitter = forms.URLField(widget=forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'Twitter'
    }),
        required=False
        )
    linkedin = forms.URLField(widget=forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'Linkedin'
    }),
        required=False
        )
    youtube = forms.URLField(widget=forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'Youtube'
    }),
        required=False
    )

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class':'form-control', 
        }),
        required=False
    )


    class Meta:
        model = Teacher
        fields = ['first_name','last_name','title','description','facebook','twitter','linkedin','youtube','image']
