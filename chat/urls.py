from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_view, name='home'),
    
    # profile 
    path('profile/', views.profile_view, name='profile'),
    
    # buy coin
    path('coin_purchase/', views.coin_purchase_view, name='coin_purchase'),
    
    # withdraw from wallet account
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    
    # chat
    path('chat/<int:chat_id>/', views.chat_view, name='chat'),
    
    # group chat
    path('group_chat/<int:group_chat_id>/', views.group_chat_view, name='group_chat'),

    # create gp (public)
    path('create_group_chat/', views.create_group_chat_view, name='create_group_chat'),
    
    # public chatroom list 
    path('public_chat_rooms/', views.public_chat_room_list_view, name='public_chat_room_list'),
    
    # join a public group 
    path('join_group/<int:group_chat_id>/', views.join_group_view, name='join_group'),
    
    # private chatroom list 
    path('private_chat_rooms/', views.private_chat_room_list_view, name='private_chat_room_list'),

    # send request for PV
    path('private/request/', views.send_private_chat_request, name='send_private_chat_request'),
    
    # accept the PV request 
    path('private/accept/<int:request_id>/', views.accept_private_chat_request, name='accept_private_chat_request'),
    
    # dont accept the PV request
    path('private/decline/<int:request_id>/', views.decline_private_chat_request, name='decline_private_chat_request'),

    # registering
    path('register/', views.register_view, name='register'),

    # login 
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    path('public_chat/<int:room_id>/', views.public_chat_view, name='public_chat'),
    path('private_chat/<int:room_id>/', views.private_chat_view, name='private_chat'),
    # path('request_private_chat/<int:user_id>/', views.request_private_chat_view, name='request_private_chat'),
    path('private_chat_list', views.private_chat_room_list_view, name='private_chat_room_list'),
    
    # call - block - report urls
    path('report/<int:reported_user_id>/', views.report_view, name='report_user'),
    path('block/<int:blocked_user_id>/', views.block_view, name='block_user'),
    path('call/<int:callee_user_id>/', views.call_view, name='call_user'),
]
