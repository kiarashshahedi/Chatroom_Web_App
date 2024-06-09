from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, CoinPurchase, Wallet, Withdrawal, Chat, Message, GroupChat, Like, Report, Block, Call, PrivateChatRoom, PublicChatRoom
from .forms import UserForm, ProfileForm, CoinPurchaseForm, WithdrawalForm, MessageForm, GroupChatForm, UserRegistrationForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


def home_view(request):
    return render(request, 'chatroom/home.html')

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

@login_required
def create_group_chat_view(request):
    if request.method == 'POST':
        form = GroupChatForm(request.POST)
        if form.is_valid():
            group_chat = form.save()
            group_chat.members.add(request.user.profile)
            group_chat.save()
            return redirect('group_chat', group_chat_id=group_chat.id)
    else:
        form = GroupChatForm()
    return render(request, 'chatroom/create_group_chat.html', {'form': form})




def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(
                user=new_user,
                birthdate=user_form.cleaned_data['birthdate'],
                distance=0  # Default value for distance
            )
            return render(request, 'chatroom/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'chatroom/register.html', {'user_form': user_form})





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

@login_required
def request_private_chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if request.user == other_user:
        return redirect('home')
    room, created = PrivateChatRoom.objects.get_or_create(user1=request.user, user2=other_user)
    return redirect('chatroom/private_chat', room_id=room.id)


def public_chat_room_list_view(request):
    rooms = PublicChatRoom.objects.all()
    return render(request, 'chatroom/public_chat_room_list.html', {'rooms': rooms})

def private_chat_room_list_view(request):
    rooms = PrivateChatRoom.objects.filter(user1=request.user) | PrivateChatRoom.objects.filter(user2=request.user)
    return render(request, 'chatroom/private_chat_room_list.html', {'rooms': rooms})