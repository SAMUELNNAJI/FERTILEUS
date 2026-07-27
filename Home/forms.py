from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'disc-input',
                'placeholder': 'Your name (or leave blank to stay anonymous)',
                'maxlength': '80',
            }),
            'body': forms.Textarea(attrs={
                'class': 'disc-textarea',
                'placeholder': 'Share your experience or ask the community a question…',
                'maxlength': '1200',
                'rows': '5',
                'id': 'comment-body',
                'required': True,
            }),
        }
        labels = {
            'name': '',
            'body': '',
        }
