from django.contrib import admin
from .models import Faculty,Student,LeaveRequest,LeaveRecord,Subject,SelectedSubject
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(LeaveRequest)
admin.site.register(LeaveRecord)
admin.site.register(Subject)
admin.site.register(SelectedSubject)
#pass=admin, adminadmin
