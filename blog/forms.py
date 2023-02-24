from django import forms
from django.forms import ModelForm
from .models import Blog, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ""


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'text', 'photo')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name...'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title of the post...'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type something...'})}

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['title'].widget.attrs['style'] = 'width:830px;'
        self.fields['text'].widget.attrs['style'] = 'width:600px;'


class BlogChangeForm(forms.ModelForm):
    photo = forms.ImageField(label="")

    class Meta:
        model = Blog
        fields = ['text', 'photo']
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type something...'})}

    def __init__(self, *args, **kwargs):
        super(BlogChangeForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['text'].widget.attrs['style'] = 'width:600px;'
