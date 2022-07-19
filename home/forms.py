from django import forms
from .models import Post, Comment

class UpdateCreatPostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        widgets = {
            "body": forms.Textarea()
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            "body": forms.Textarea()
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            "body": forms.Textarea()
        }