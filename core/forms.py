from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment, MentorshipRequest


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_image', 'location', 'visibility_mode', 'is_mentor', 'skills', 'equity_badges']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'visibility_mode': forms.Select(attrs={'class': 'form-select'}),
            'is_mentor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'skills': forms.CheckboxSelectMultiple(),
            'equity_badges': forms.CheckboxSelectMultiple(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['hub', 'title', 'content', 'post_type', 'video_url', 'is_anonymous']
        widgets = {
            'hub': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Give your post a clear title...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8,
                                             'placeholder': 'Share your knowledge, ask questions, or tell your story...'}),
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'video_url': forms.URLInput(
                attrs={'class': 'form-control', 'placeholder': 'Optional: YouTube or Vimeo link'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts or answer the question...'
            }),
        }


class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ['topic', 'message']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Career transition to tech'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Introduce yourself and explain what you hope to learn...'
            }),
        }