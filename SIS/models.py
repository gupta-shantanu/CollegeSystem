from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,User

class Faculty(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    photo=models.FileField()
    specialization=models.CharField(max_length=100)
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.user.username})


class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    photo=models.FileField(blank=True, null=True)
    DOB=models.DateField()
    tenth_marks=models.FloatField(default=0)
    inter_marks=models.FloatField(default=0)
    current_marks=models.FloatField(default=0)
    branch = models.CharField(max_length=100,
        choices=(('Computer Science & Engineering','Computer Science & Engineering'),('Electrical Engineering','Electrical Engineering'),('Civil Engineering','Civil Engineering'),('Others','Others')),
        default='Computer Science & Engineering',
        )

    year = models.IntegerField(
        choices=((1,'Ist Year'),(2,'IInd Year'),(3,'IIIrd Year'),(4,'IVth Year')),
        default=1,
        )
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.user.username})

class LeaveRequest(models.Model):
    faculty=models.ForeignKey(to=Faculty, related_name="request", null=True, blank=True)
    start=models.DateField()
    end=models.DateField()
    type=models.IntegerField(
        choices=((1,"Sick"),(2,'Casual'),(3,'Earned')),
        default=3,
        )
    status=models.IntegerField(
        choices=((1,"Accepted"),(2,'Rejected'),(3,'Pending')),
        default=3,
        )
    reason=models.CharField(max_length=900)
    verdict=models.CharField(max_length=900,null=True)
    def days(self):
        return (self.end-self.start).days


class LeaveRecord(models.Model):
    faculty=models.OneToOneField(Faculty,on_delete=models.CASCADE,null=True)
    casual_leave=models.IntegerField(default=7)
    earned_leave=models.IntegerField(default=10)
    sick_leave=models.IntegerField(default=8)



class Subject(models.Model):
    subject_name=models.CharField(max_length=100)
    faculty=models.ForeignKey(to=Faculty, related_name="teaches", null=True, blank=True)

class SelectedSubject(models.Model):
    subject=models.ForeignKey(to=Subject, related_name="studies", null=True, blank=True)
    student=models.ForeignKey(to=Student, related_name="selected", null=True, blank=True)

    def percentage(self):
        p,a=self.present(),self.absent()
        s=p+a
        if s!=0:
            return str(round(p*100.0/s,2))+"%"
        else:
            return 'N.A'
    def present(self):
        a=self.attendance.all()
        return a.filter(present=True).count()
    def absent(self):
        a=self.attendance.all()
        return a.filter(present=False).count()
    def eligiblity(self):
        if self.percentage()=='N.A':
            return False
        return float(self.percentage()[:-1])>60
    def timesheet(self):
        return self.attendance.all().order_by('Date')

    


class AttendanceRecord(models.Model):
    selected_subject=models.ForeignKey(to=SelectedSubject, related_name="attendance", null=True, blank=True)
    Date=models.DateField(null=True)
    present=models.BooleanField()