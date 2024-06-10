from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Wallet, Chat, Message, GroupChat, PrivateChatRoom, PublicChatRoom, PrivateChatRequest, Like, Report, Block, Call, Withdrawal, CoinPurchase
from .forms import UserForm, ProfileForm, CoinPurchaseForm, WithdrawalForm, MessageForm, GroupChatForm, UserRegistrationForm, CallForm, BlockForm, ReportForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import IntegrityError




# Home page
@login_required
def home_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'chatroom/home.html', context)


# Profile page
@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'chatroom/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# buy coins page
@login_required
def coin_purchase_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = CoinPurchaseForm(request.POST)
        if form.is_valid():
            coin_purchase = form.save(commit=False)
            coin_purchase.profile = profile
            # Add logic for processing payment here
            coin_purchase.save()
            profile.coins += coin_purchase.coins
            profile.save()
            return redirect('profile')
    else:
        form = CoinPurchaseForm()
    return render(request, 'chatroom/coin_purchase.html', {'form': form})



# bardasht az hesab 
@login_required
def withdrawal_view(request):
    wallet = get_object_or_404(Wallet, profile__user=request.user)
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.wallet = wallet
            # Add logic for processing withdrawal here
            withdrawal.save()
            return redirect('wallet')
    else:
        form = WithdrawalForm()
    return render(request, 'chatroom/withdrawal.html', {'form': form})



# chat page
@login_required
def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants__user=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user.profile
            message.save()
            return redirect('chat', chat_id=chat.id)
    else:
        form = MessageForm()
    messages = chat.message_set.all()
    return render(request, 'chatroom/chat.html', {'form': form, 'chat': chat, 'messages': messages})



# gp chat page
@login_required
def group_chat_view(request, group_chat_id):
    group_chat = get_object_or_404(GroupChat, id=group_chat_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = group_chat
            message.sender = request.user.profile
            message.save()
            return redirect('group_chat', group_chat_id=group_chat.id)
    else:
        form = MessageForm()
    messages = group_chat.message_set.all()
    return render(request, 'chatroom/group_chat.html', {'form': form, 'group_chat': group_chat, 'messages': messages})



# user register page
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user, coins=20)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



# public chat page 
@login_required
def public_chat_view(request, room_id):
    room = get_object_or_404(PublicChatRoom, id=room_id)
    messages = Message.objects.filter(public_chat_room=room)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.public_chat_room = room
            message.save()
            return redirect('public_chat', room_id=room.id)
    else:
        form = MessageForm()
    return render(request, 'chatroom/public_chat.html', {'room': room, 'messages': messages, 'form': form})



# private chat page
@login_required
def private_chat_view(request, room_id):
    room = get_object_or_404(PrivateChatRoom, id=room_id)
    if request.user != room.user1 and request.user != room.user2:
        return redirect('home')
    messages = Message.objects.filter(private_chat_room=room)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.private_chat_room = room
            message.save()
            return redirect('private_chat', room_id=room.id)
    else:
        form = MessageForm()
    return render(request, 'chatroom/private_chat.html', {'room': room, 'messages': messages, 'form': form})


# send request for connecting in pv
@login_required
def request_private_chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if request.user == other_user:
        return redirect('home')
    room, created = PrivateChatRoom.objects.get_or_create(user1=request.user, user2=other_user)
    return redirect('chatroom/private_chat', room_id=room.id)

# list of public chats
@login_required
def public_chat_room_list_view(request):
    groups = GroupChat.objects.all()
    return render(request, 'chatroom/public_chat_room_list.html', {'groups': groups})

# list of private chats
@login_required
def private_chat_room_list_view(request):
    rooms = PrivateChatRoom.objects.filter(user1=request.user) | PrivateChatRoom.objects.filter(user2=request.user)
    received_requests = PrivateChatRequest.objects.filter(recipient=request.user, accepted=False)
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chatroom/private_chat_room_list.html', {
        'rooms': rooms,
        'received_requests': received_requests,
        'users': users,
    })

# send request for connecting in pv
@login_required
def send_private_chat_request(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        recipient = get_object_or_404(User, id=recipient_id)
        if request.user.profile.coins >= 1:
            request.user.profile.coins -= 1
            request.user.profile.save()
            PrivateChatRequest.objects.create(requester=request.user, recipient=recipient)
            messages.success(request, 'Private chat request sent.')
        else:
            messages.error(request, 'You do not have enough coins to send a private chat request.')
    return redirect('private_chat_room_list')

# accept the to chat in pv
@login_required
def accept_private_chat_request(request, request_id):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id, recipient=request.user)
    if chat_request.accepted:
        messages.error(request, 'This request has already been accepted.')
    else:
        PrivateChatRoom.objects.create(user1=chat_request.requester, user2=chat_request.recipient)
        chat_request.accepted = True
        chat_request.save()
        messages.success(request, 'Private chat request accepted.')
    return redirect('private_chat_room_list')

# dont accept to chat in pv
@login_required
def decline_private_chat_request(request, request_id):
    chat_request = get_object_or_404(PrivateChatRequest, id=request_id, recipient=request.user)
    chat_request.delete()
    messages.success(request, 'Private chat request declined.')
    return redirect('private_chat_room_list')



# making group chat (public)
@login_required
def create_group_chat_view(request):
    if request.method == 'POST':
        form = GroupChatForm(request.POST)
        if form.is_valid():
            group_chat = form.save(commit=False)
            group_chat.owner = request.user
            group_chat.save()
            messages.success(request, 'Group chat created successfully!')
            return redirect('public_chat_room_list')
        else:
            for field in form:
                for error in field.errors:
                    print(f"Error in {field.name}: {error}")
            messages.error(request, 'There was an error creating the group chat.')
    else:
        form = GroupChatForm()
    return render(request, 'chatroom/create_group_chat.html', {'form': form})


# Join a public group view
@login_required
def join_group_view(request, group_chat_id):
    group = get_object_or_404(GroupChat, id=group_chat_id)
    profile = Profile.objects.get(user=request.user)
    group.members.add(profile)
    return redirect('group_chat', group_chat_id=group_chat_id)


@login_required
def group_chat_view(request, group_chat_id):
    group = get_object_or_404(GroupChat, id=group_chat_id)
    messages = Message.objects.filter(group_chat=group)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            form.save()
            return redirect('group_chat', group_chat_id=group_chat_id)
    else:
        form = MessageForm(user=request.user)  # Pass the user to the form

    return render(request, 'chatroom/group_chat.html', {
        'group': group,
        'messages': messages,
        'form': form,
    })
    
    
    
    
def report_view(request, reported_user_id):
    reported_user = get_object_or_404(User, id=reported_user_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user.profile
            report.reported = reported_user.profile
            report.save()
            messages.success(request, 'Report submitted successfully.')
            return redirect('home')
    else:
        form = ReportForm()
    return render(request, 'chatroom/report.html', {'form': form, 'reported_user': reported_user})

@login_required
def block_view(request, blocked_user_id):
    blocked_user = get_object_or_404(User, id=blocked_user_id)
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            block = form.save(commit=False)
            block.blocker = request.user.profile
            block.blocked = blocked_user.profile
            block.save()
            messages.success(request, 'User blocked successfully.')
            return redirect('home')
    else:
        form = BlockForm()
    return render(request, 'chatroom/block.html', {'form': form, 'blocked_user': blocked_user})

@login_required
def call_view(request, callee_user_id):
    callee_user = get_object_or_404(User, id=callee_user_id)
    if request.method == 'POST':
        form = CallForm(request.POST)
        if form.is_valid():
            call = form.save(commit=False)
            call.caller = request.user.profile
            call.callee = callee_user.profile
            call.save()
            messages.success(request, 'Call initiated successfully.')
            return redirect('home')
    else:
        form = CallForm()
    return render(request, 'chatroom/call.html', {'form': form, 'callee_user': callee_user})