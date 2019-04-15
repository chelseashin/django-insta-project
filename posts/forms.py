from django import forms
from .models import Post, Image, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content',]

class ImageForm(forms.ModelForm):
    # widgets은 밖으로 빼주는 것을 권장
    file = forms.ImageField(widget = forms.FileInput(attrs={'multiple' : True, }))
    class Meta:
        model = Image
        fields = ['file',]
        # widgets = {
        #     'file' : forms.FileInput(attrs={'multiple' : True}),
        # }

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="")
    class Meta:
        model = Comment
        fields = ['content',]