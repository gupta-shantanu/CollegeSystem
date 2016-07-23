from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView,View
from django.views.generic import DetailView
from .models import *

from .forms import StudentForm, FacultyForm, UserForm
from .models import Student, Faculty

def home(request):
    return render(request,'index.html')

class Detail(DetailView):
    model=User
    template_name='detail.html'



class FacultyFormView(View):
    form_class=FacultyForm
    template_name='register.html'
    def get(self,request,id):
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request,id):
        print("check")
        form=self.form_class(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.user=User.objects.get(pk=self.kwargs['id'])
            user.save()
            redirect("detail",username=user.user.username)
        return render(request,self.template_name,{'form':form})

class StudentFormView(View):
    form_class=StudentForm
    template_name='register.html'
    def get(self,request,id):
        User.objects.get(id=self.kwargs['id'])
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request,id):
        form=self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            user=form.save(commit=False)
            obj=User.objects.get(id=self.kwargs['id'])
            user.user=obj
            user.save()
            redirect("detail",username=user.user.username)
                
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
            # if self.kwargs['teacher'] :
            #     return redirect("teacherform",user=user.id)
            # else:
            return redirect("studentform",id=user.id)

        return render(request,self.template_name,{'form':form})


