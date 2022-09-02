from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'content']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("title")
        if len(description) > 255:
            raise ValidationError({
                "title": "Максимальная длина заголовка 255 символов"
            })

        return cleaned_data


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        if len(description) > 255:
            raise ValidationError({
                "text": "Сообщение слишком длинное (максимальная длина 255 символов)"
            })

        return cleaned_data
