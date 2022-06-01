
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets

from .models import Article, Category, Comment

choices = Category.objects.all().values_list('name','name')

choice_list = []

for item in choices:
    choice_list.append(item)



class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","author", "content","image", "tags", "category", "snippet"]
        widgets = {
            'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'author': forms.TextInput(attrs={'class':'form-control', 'value':'','id':'zayyad', 'type':'hidden'}),
            'snippet' : forms.Textarea(attrs={'class':'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter your Name', 'class':'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter your Email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}

class PostSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['c'].label = 'Category'
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'})