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
    branch = models.IntegerField(
        choices=((1,'Computer Science & Engineering'),(2,'Electrical Engineering'),(3,'Civil Engineering'),(4,'Others')),
        default=1,
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

class AttendanceRecord(models.Model):
    student=models.ForeignKey(to=Student, related_name="student", null=True, blank=True)
    subject=models.IntegerField(default=0)
    Date=models.DateField()
    present=models.BooleanField()

class Subject(models.Model):
    subject_name=models.CharField(max_length=100)
    faculty=models.ForeignKey(to=Faculty, related_name="teaches", null=True, blank=True)

class SelectedSubject(models.Model):
    subject=models.ForeignKey(to=Subject, related_name="studies", null=True, blank=True)
    student=models.ForeignKey(to=Student, related_name="selected", null=True, blank=True)
    
