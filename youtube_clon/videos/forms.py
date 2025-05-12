from django import forms
from .models import Video, Comment # Імпорти об'єднано

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Напишіть свій коментар тут...',
                'class': 'form-control'
            }),
        }
        labels = {
            'text': ''
        }