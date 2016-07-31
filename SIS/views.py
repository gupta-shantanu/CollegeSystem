from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView,View
from django.views.generic import DetailView,ListView
from django.db.models import Q
from .models import *

from .forms import StudentForm, FacultyForm, UserForm, LeaveRequestForm

def home(request):
    return render(request,'index.html')

def requestverdict(request):
    return render(request,'index.html')

def myprofile(request):
    return render(request,'index.html')

def logout_view(request):
    logout(request)

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
    @method_decorator(login_required)
    def get(self,request):
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    @method_decorator(login_required)
    def post(self,request):
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
    @method_decorator(login_required)
    def get(self,request):
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    @method_decorator(login_required)
    def post(self,request):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            obj=request.user
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
            auth=authenticate(username=user.username,password=password)
            if auth:
                if auth.is_active:
                    login(request,auth)
                    if user.is_staff:
                        return redirect("teacherform")
                    return redirect("studentform")

        return render(request,self.template_name,{'form':form})

class SearchView(ListView):
    template_name = 'userList.html'
    model = User

    def get_queryset(self):
        try:
            name = self.request.GET.get('q')
        except:
            name = ''
        if (name != ''):

            object_list = self.model.objects.filter(Q(first_name__icontains = name )|Q(username__icontains = name )).exclude(username='admin')
        else:
            object_list = self.model.objects.all().exclude(username='admin')
        return object_list


class LeaveFormView(View):
    form_class=LeaveRequestForm
    template_name='register.html'
    @method_decorator(login_required)
    def get(self,request):
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    @method_decorator(login_required)
    def post(self,request):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            re=form.save(commit=False)
            re.user=request.user
            re.save()
            # return redirect("profile")

        return render(request,self.template_name,{'form':form})

