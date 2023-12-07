from django import forms

from .models import *


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Заголовок'
        self.fields['text'].label = 'Текст'
        self.fields['category'].label = 'Категория'
        self.fields['post_category'].label = 'Тип'
        self.fields['author'].label = 'Автор'

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
            'post_category',
            'author',
       ]
