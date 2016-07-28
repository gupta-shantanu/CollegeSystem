from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView,View
from django.views.generic import DetailView,ListView
from .models import *

from .forms import StudentForm, FacultyForm, UserForm

def home(request):
    return render(request,'index.html')

class Detail(DetailView):
    model=User
    template_name='detail.html'
    slug_field = 'username'

class Info(DetailView):
    model=User
    template_name='detail.html'

class StudentList(ListView):
    template_name='list.html'
    context_object_name = 'student'

    def get_queryset(self):
        return Student.objects.all()


class FacultyList(ListView):
    template_name='list.html'
    context_object_name = 'faculty'

    def get_queryset(self):
        return Faculty.objects.all()

class RequestList(ListView):
    context_object_name = 'request'
    template_name='RequestList.html'
    def get_queryset(self):
        return LeaveRequest.objects.all()


class FacultyFormView(View):
    form_class=FacultyForm
    template_name='register.html'
    def get(self,request,id):
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request,id):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.user=User.objects.get(pk=self.kwargs['id'])
            user.save()
            return redirect("detail",slug=user.user.username)
        return render(request,self.template_name,{'form':form})

class StudentFormView(View):
    form_class=StudentForm
    template_name='register.html'
    def get(self,request,id):
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request,id):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            obj=User.objects.get(id=self.kwargs['id'])
            user.user=obj
            user.save()
            return redirect("detail",slug=user.user.username)
                
        return render(request,self.template_name,{'form':form})

class UserFormView(View):
    form_class=UserForm
    template_name='register.html'
    def get(self,request):
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            password=form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            if user.is_staff:
                 return redirect("teacherform",id=user.id)
            return redirect("studentform",id=user.id)

        return render(request,self.template_name,{'form':form})


