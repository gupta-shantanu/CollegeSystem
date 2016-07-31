from django.contrib.auth.models import User
from django import forms
from .models import Student,Faculty,LeaveRequest
from django.core.urlresolvers import reverse
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget

class UserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','first_name','last_name','email','password1','password2','is_staff']

#UserCreationForm.Meta.fields +

class FacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ['photo','specialization']

class StudentForm(forms.ModelForm):

    DOB = forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1920,2010)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])

    class Meta:
        model = Student
        fields = ['photo','DOB','branch','year','tenth_marks','inter_marks','current_marks']

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start','end','type','reason']

