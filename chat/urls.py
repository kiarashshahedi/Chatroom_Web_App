from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('coin_purchase/', views.coin_purchase_view, name='coin_purchase'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    path('chat/<int:chat_id>/', views.chat_view, name='chat'),
    path('group_chat/<int:group_chat_id>/', views.group_chat_view, name='group_chat'),
    path('create_group_chat/', views.create_group_chat_view, name='create_group_chat'),
    path('register/', views.register_view, name='register'),
    path('public_chat/<int:room_id>/', views.public_chat_view, name='public_chat'),
    path('private_chat/<int:room_id>/', views.private_chat_view, name='private_chat'),
    path('request_private_chat/<int:user_id>/', views.request_private_chat_view, name='request_private_chat'),
    path('public_chat_list', views.public_chat_room_list_view, name='public_chat_room_list'),
    path('private_chat_list', views.private_chat_room_list_view, name='private_chat_room_list')

    

]
