from django.urls import path
from . import views

urlpatterns = [
    # path('room/', views.room_view, name='room_view'),
    path('room/', views.room, name='room'),
    path('supervisor-room/<supervisor_user>/<int:room_id>', views.supervisor_room, name='supervisor_room'),
    path('supervisor-room/<supervisor_user>/',views.supervisor_room2, name="supervisor_room2")
]
