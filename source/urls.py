from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from SIS.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', StudentFormView.as_view(), name='index'),
    url(r'^login$', auth_views.login, {'template_name': 'login.html'},name='login'),
    url(r'^logout$', auth_views.logout, name='logout'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'register$', UserFormView.as_view(), name='register'),
    url(r'index.html$', StudentFormView.as_view(), name='index'),
    url(r'^register/student$', StudentFormView.as_view(), name='studentform'),
    url(r'^register/faculty$', FacultyFormView.as_view(), name='teacherform'),
    url(r'^info/(?P<id>[0-9]+)$', Info.as_view(), name='info'),
    url(r'^profile$', myprofile, name='profile'),
    url(r'^list/faculty$', FacultyList.as_view(), name='facultylist'),
    url(r'^list/students$', StudentList.as_view(), name='studentlist'),
    url(r'^request$', LeaveFormView.as_view(), name='newLeave'),
    url(r'^response$', requestverdict, name='request_verdict'),
    url(r'^RequestList$', RequestList.as_view(), name='RequestList'),
    url(r'^(?P<slug>[a-z0-9]+)$', Detail.as_view(), name='detail'),
    url(r'^attendance$', Detail.as_view(), name='fillAttendance'),

]

urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

