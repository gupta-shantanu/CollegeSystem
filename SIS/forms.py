from django.contrib.auth.models import User
from django import forms
from .models import Student,Faculty
from django.core.urlresolvers import reverse
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','first_name','last_name','email','password1','password2','is_staff']

#UserCreationForm.Meta.fields +

class FacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ['photo','department']

class StudentForm(forms.ModelForm):
    DOB=forms.DateField(input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y']) #widget=AdminDateWidget,
    class Meta:
        model = Student
        fields = ['photo','DOB','branch','year']
