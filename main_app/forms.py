from django import forms
from .models import Comment, UserProfile, CommentSection, Watchlist
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'image', 'city', 'website', 'linkedin', 'twitter', 'tiktok', 'github', 'discord')

        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            # 'image': forms.Textarea(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control'}),
            'tiktok': forms.TextInput(attrs={'class': 'form-control'}),
            'github': forms.TextInput(attrs={'class': 'form-control'}),
            'discord': forms.TextInput(attrs={'class': 'form-control'})
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('image','body',)

        widget = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_active = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-input'}))
    # password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')


class PasswordChanged(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password')

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = CommentSection
        fields = ('image','body',)

        widget = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }

class AddWatchlist(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ('user', 'movie_id')