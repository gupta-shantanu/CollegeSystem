from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from SIS.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^home$', homepage, name='homepage'),
    url(r'^login$', auth_views.login, {'template_name': 'login.html'},name='login'),
    url(r'^logout$', auth_views.logout, {'next_page' : '/login'},name='logout'),
    url(r'^accounts/login$', loginFirst, name='loginfirst'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'register$', UserFormView.as_view(), name='register'),
    url(r'index.html$', home, name='index'),
    url(r'^register/student$', StudentFormView.as_view(), name='studentform'),
    url(r'^register/faculty$', FacultyFormView.as_view(), name='teacherform'),
    url(r'^info/(?P<id>[0-9]+)$', Info.as_view(), name='info'),
    url(r'^profile$', myprofile, name='profile'),
    url(r'^list/faculty$', FacultyList.as_view(), name='facultylist'),
    url(r'^list/students$', StudentList.as_view(), name='studentlist'),
    url(r'^student/update/(?P<pk>[\-\d]+)$', StudentUpdate.as_view(), name='studentupdate'),
    url(r'^faculty/update/(?P<pk>[\-\d]+)$', FacultyUpdate.as_view(), name='facultyupdate'),
    url(r'^update/(?P<slug>[\-\w]+)$', UserUpdate.as_view(), name='userupdate'),
    url(r'^request$', LeaveFormView.as_view(), name='newLeave'),
    url(r'^addsubject$', newSubject, name='newSubject'),
    url(r'^selectsubject/(?P<id>[\-\d]+)$', newSelectedSubject, name='selectSubject'),
    url(r'^response$', requestverdict, name='request_verdict'),
    url(r'^RequestList$', RequestList.as_view(), name='RequestList'),
    url(r'^timesheet/(?P<id>[\-\d]+)$', PublicTimesheet, name='publicTimesheet'),
    url(r'^timesheet$', Timesheet, name='timesheet'),
    url(r'^attendance/(?P<subject>[\-\w]+)$', fillAttendance, name='fillAttendance'),
    url(r'^attendance/list/(?P<subject>[\-\w]+)$', viewAttendance , name='viewAttendance'),
    url(r'^(?P<slug>[a-z0-9]+)$', Detail.as_view(), name='detail'),

]

urlpatterns +=[
    url(r'^accounts/password/reset/$', auth_views.password_reset, {'template_name': 'update_form.html'}),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}),
    url(r'^user/password/reset/$',auth_views.password_reset,{'post_reset_redirect' : '/user/password/reset/done/'},name="password_reset"),
    url(r'^user/password/reset/done/$',auth_views.password_reset_done,name="password_reset_done"),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',auth_views.password_reset_confirm,{'post_reset_redirect' : '/user/password/done/'},name="password_reset_confirm"),
    url(r'^user/password/done/$',auth_views.password_reset_complete,name="password_reset_done"),
]

urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

