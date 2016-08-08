from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse,reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views.generic.edit import CreateView, UpdateView, DeleteView,View
from django.views.generic import DetailView,ListView
from django.db.models import Q
from .models import *
import datetime
from django.forms import DateField,SelectDateWidget
from django import forms

from .forms import StudentForm, FacultyForm, UserForm, LeaveRequestForm
class dates(forms.Form):
        date = DateField(widget=
        SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
        initial=datetime.date.today)

def home(request):
    return render(request,'home.html')

def homepage(request):
    return render(request,'login/home.html')

def loginFirst(request):
    return redirect("login")

@login_required
def Timesheet(request):
    return render(request,'login/timesheet.html',{'student':request.user.student})

@login_required
def PublicTimesheet(request,id):
    return render(request,'login/timesheet.html',{'student':Student.objects.get(id=id)})

@login_required
def requestverdict(request):

    if request.POST.get('accept'):
        result=1
    else:
        result=2
    r=LeaveRequest.objects.get(id=request.POST.get('request_id'))
    r.status=result
    r.verdict=request.POST.get('reason')
    r.save()
    records=LeaveRecord.objects.get(faculty=r.faculty)
    if r.type==1:
        records.sick_leave-=1
    elif r.type==2:
        records.casual_leave-=1
    elif r.type==2:
        records.earned_leave-=1
    records.save()

    return redirect("RequestList")

@login_required
def fillAttendance(request,subject):

        if request.POST.get('submit'):
            dt=datetime.date(year=int(request.POST.get('date_year')),month=int(request.POST.get('date_month')),day=int(request.POST.get('date_day')))
            for p in request.POST.keys():
                if p[0:4]=='att_':
                    selsub=SelectedSubject.objects.get(id=p[4:])
                    pr= True if(request.POST.get('check_'+p[4:])) else False
                    r=AttendanceRecord(selected_subject=selsub,present=pr,Date=dt)
                    r.save()
            return redirect("profile")
        else:
            sub=Subject.objects.get(subject_name=subject,faculty=request.user.faculty)
            selsub=SelectedSubject.objects.filter(subject=sub)
            return render(request,'login/fill_attendance.html',{'selected_subject':selsub,'subject':subject,'day':dates()})

@login_required
def viewAttendance(request,subject):
    try:
        sub=Subject.objects.get(subject_name=subject,faculty=request.user.faculty)
    except:
        return redirect("profile")
    return render(request,'login/view_attendance.html',{'list':sub.studies.all(),'subject':subject})



@login_required
def newSelectedSubject(request,id):
    sub=Subject.objects.get(id=id)
    try:
        SelectedSubject.objects.get_or_create(student=request.user.student,subject=sub)
    except:
        Subject.objects.get_or_create(faculty=request.user.faculty,subject_name=sub.subject_name)

    return redirect("profile")

@login_required
def newSubject(request):
    newsub=request.POST.get('name')
    if newsub:
        newsub=newsub.replace(' ','_')
        newsub=newsub.replace(r"'",'')

        Subject.objects.get_or_create(faculty=request.user.faculty,subject_name=newsub.lower())


    return redirect("profile")




@login_required
def myprofile(request):

    return render(request,'login/profile.html',{'user':request.user,'subjects':Subject.objects.all(),'day':datetime.date.today})

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
    context_object_name = 'student'

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
            user.user=request.user
            user.save()
            LeaveRecord(faculty=user).save()
            return redirect("profile")
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
            return redirect("profile")
                
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
    template_name='RequestForm.html'
    @method_decorator(login_required)
    def get(self,request):
        form= self.form_class(None)
        return render(request,self.template_name,{'form':form})
    @method_decorator(login_required)
    def post(self,request):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            re=form.save(commit=False)
            re.faculty=request.user.faculty
            re.save()
            return redirect("profile")

        return render(request,self.template_name,{'form':form})


class FacultyUpdate(UpdateView):
    model = Faculty
    
    fields = ['specialization','photo']
    template_name = 'update_form.html'
    success_url = reverse_lazy('profile')
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object == request.user.faculty
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('profile')
        return super(FacultyUpdate, self).dispatch(
            request, *args, **kwargs)

class StudentUpdate(UpdateView):
    model = Student
    fields = ['photo','DOB','branch','year','tenth_marks','inter_marks','current_marks']
    template_name = 'update_form.html'
    success_url = reverse_lazy('profile')
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object == request.user.student
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('profile')
        return super(StudentUpdate, self).dispatch(
            request, *args, **kwargs)



class UserUpdate(UpdateView):
    model = User
    slug_field = 'username'
    fields = ['first_name','last_name','email']
    template_name = 'update_form.html'
    success_url = reverse_lazy('profile')
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('profile')
        return super(UserUpdate, self).dispatch(
            request, *args, **kwargs)



