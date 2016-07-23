from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,User

class Faculty(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    department = models.CharField(max_length=100)
    photo=models.FileField()
    def get_absolute_url(self):
        return reverse('detail', kwargs={'username': self.user.username})


class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    photo=models.FileField(blank=True, null=True)
    attendance=models.IntegerField(default=0)
    DOB=models.DateField()
    branch = models.IntegerField(
        choices=((1,'Computer Science & Engineering'),(2,'Electrical Engineering'),(3,'Civil Engineering'),(4,'Others')),
        default=1,
        )

    year = models.IntegerField(
        choices=((1,'Ist Year'),(2,'IInd Year'),(3,'IIIrd Year'),(4,'IVth Year')),
        default=1,
        )
    def get_absolute_url(self):
        return reverse('detail', kwargs={'username': self.user.username})

