from .models import Comment
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


choices = Category.objects.all().values_list('name','name')

choice_list = []

for item in choices:
    choice_list.append(item)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']





class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","author", "content","image", "tags", "category", "snippet"]
        widgets = {
            'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'author': forms.TextInput(attrs={'class':'form-control', 'value':'','id':'zayyad', 'type':'hidden'}),
            'snippet' : forms.Textarea(attrs={'class':'form-control'}),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('email','body')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}
