
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .views import home
from django.urls import path
from .views import (admin_login,  admin_logout, admin_dashboard,staff_login, staff_logout,staff_dashboard)
from . import views
from diagnostic_centers.views import *

admin.site.site_header = 'LMS'                   
admin.site.index_title = 'LMS'                
admin.site.site_title = 'LMS'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('custom_users.urls', namespace='custom_users')),
    path('', include('diagnostic_centers.urls', namespace='diagnostic_centers')),
    path('accounts/', include('allauth.urls')),

    path('supervisor-login/', admin_login, name='admin-login'),
    path('supervisor-logout/', admin_logout, name='admin-logout'),
    path('supervisor-dashboard/<username>/', admin_dashboard, name='admin-dashboard'),
    path('supervisor-chat/',views.supervisor_chat, name="supervisor_chat"),
    path('student-login/', staff_login, name='staff-login'),
    path('student-logout/', staff_logout, name='staff-logout'),
    path('student-dashboard/<username>/', staff_dashboard, name='staff-dashboard'),
    path('student-dashboard/<int:id>/<username>/', staff_dashboard, name='staff-dashboards'),
    path('chat/',views.chat, name="chat"),
    path('load-messages/', views.load_messages, name='load_messages'),
    path('questionnaire/', questionnaire, name='questionnaire'),

   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


