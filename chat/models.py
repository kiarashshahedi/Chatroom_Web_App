# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True, default=0)
    is_online = models.BooleanField(default=False)
    last_online = models.DateTimeField(auto_now=True)
    coins = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    photos = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class CoinPurchase(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    coins = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)



class Wallet(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    shaba_number = models.CharField(max_length=24)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)



class Withdrawal(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    fee = models.DecimalField(max_digits=10, decimal_places=2)




class Chat(models.Model):
    participants = models.ManyToManyField(Profile, related_name='chats')
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(default=timezone.timedelta(hours=24))
    
    
    

class GroupChat(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(Profile, related_name='group_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
    

class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_likes')
    liked_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='given_likes')
    timestamp = models.DateTimeField(auto_now_add=True)




class Report(models.Model):
    reporter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reports_made')
    reported = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)




class Block(models.Model):
    blocker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blocks_made')
    blocked = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blocks_received')
    timestamp = models.DateTimeField(auto_now_add=True)




class Call(models.Model):
    caller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='calls_made')
    callee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='calls_received')
    is_video = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
    cost = models.IntegerField()
    
    
    
    
class PublicChatRoom(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(User, related_name='private_chat_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='private_chat_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_extended_at = models.DateTimeField(auto_now_add=True)
    
    def needs_extension(self):
        return timezone.now() > self.last_extended_at + timedelta(hours=24)

    def extend_chat(self):
        self.last_extended_at = timezone.now()
        self.save()





class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey('Profile', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    public_chat_room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    private_chat_room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    voice = models.FileField(upload_to='voices/', null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)





class PrivateChatRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)