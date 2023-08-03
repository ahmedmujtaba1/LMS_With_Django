from django.urls import path

from .views import ( profile,    profile_edit)

app_name = 'custom_users'

urlpatterns = [
    # path('login/', MyLoginView.as_view(), name='account_login'),
    path('profile/', profile, name='profile'),
    path('profile-edit/', profile_edit, name='profile-edit'),
]

