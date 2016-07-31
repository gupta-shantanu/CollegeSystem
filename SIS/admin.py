from django.contrib import admin
from .models import Faculty,Student,LeaveRequest,LeaveRecord
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(LeaveRequest)
admin.site.register(LeaveRecord)
#pass=admin, adminadmin