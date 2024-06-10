from django import forms
from django.contrib.auth.models import User
from .models import Profile, CoinPurchase, Withdrawal, Message, GroupChat, Call, Block, Report
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'name', 'birthdate', 'city', 'education', 'skills', 'bio', 'distance', 'photos', 'phone_number', 'address']


class CoinPurchaseForm(forms.ModelForm):
    class Meta:
        model = CoinPurchase
        fields = ['coins']

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['amount']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Include any other fields you want in the form
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from the kwargs
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # Assign the user to the message
        if commit:
            instance.save()
        return instance

class GroupChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = ['name', 'capacity']



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birthdate']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    
class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = ['is_video', 'duration', 'cost']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']

class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = []