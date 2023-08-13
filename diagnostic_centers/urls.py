from django.urls import path
from .views import (admin_login,  admin_logout, admin_dashboard,staff_login, staff_logout,staff_dashboard)
from .views import q
from . import views
app_name = 'diagnostic_centers'


from django.urls import path
from .views import admin_dashboard

from django.urls import path
from . import views


from django.urls import path
from . import views



# urls.py
from django.urls import path
from . import views




urlpatterns = [
    path('supervisor-login/', admin_login, name='admin-login'),
    path('supervisor-logout/', admin_logout, name='admin-logout'),
    path('supervisor-dashboard/<username>/', admin_dashboard, name='admin-dashboard'),

    path('student-login/', staff_login, name='staff-login'),
    path('student-logout/', staff_logout, name='staff-logout'),
    path('student-dashboard/<username>/', staff_dashboard, name='staff-dashboard'),
    path('student-dashboard/<int:id>/<username>/', staff_dashboard, name='staff-dashboards'),

 
    path('upload/', views.project_upload, name='project_upload'),
    path('list/', views.project_list, name='project_list'),

    path('project_approval/<int:upload_id>/<username>/', views.project_approval, name='project_approval'),
    

]
