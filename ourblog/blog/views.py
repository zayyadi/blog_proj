from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CommentForm, ArticleForm
from .models import Article, Comment
# from django.views.generic import (
#     ListView,
#     DetailView,
#     CreateView,
#     UpdateView,
#     DeleteView
# )
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    articles = Article.objects.all()

    return render(request,"articles.html",{"articles":articles})
# class IndexView(ListView):
#     model = Article
#     context_object_name = 'article'
#     template_name = 'index.html'
#     ordering = ['-pub_date']
#     paginate_by = 5

#     # def get_queryset(self):
#     #     user = get_object_or_404(User, username=self.kwargs.get('username'))
#     #     return Article.objects.filter(author=user).order_by('-date_posted')

#     # def get_queryset(self):
#     #     return Article.objects.order_by('-pub_date')[:10]
    
# # class ArticleDetailView(DetailView):
# #     model = Article
# #     template_name = 'article-detail.html'

# def article_post(request, pk):
#     template_name = 'article-detail.html'
#     article = get_object_or_404(Article, pk=pk)
#     comments = article.comments.filter(active=True).order_by("-created_on")
#     new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():

#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = article
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()

#     return render(request, template_name, {'article': article,
#                                         'comments': comments,
#                                         'new_comment': new_comment,
#                                         'comment_form': comment_form})

# class ArticleCreateView(LoginRequiredMixin, CreateView):
#     model = Article
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Article
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == Article.author:
#             return True
#         return False


# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Article
#     success_url = 'blog-home'

#     def test_func(self):
#         article = self.get_object()
#         if self.request.user == article.author:
#             return True
#         return False



def index(request):
    return render(request,"index.html")
    
def about(request):
    return render(request,"about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)


@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.slug = slugify(article.title)
        article.author = request.user
        article.save()

        messages.success(request,"Article created successfully")
        return redirect("blog:dashboard")
    return render(request,"addarticle.html",{"form":form})


def detail(request,slug):
    #article = Article.objects.filter(id = id).first()   
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments })


@login_required(login_url = "user:login")
def updateArticle(request, slug):

    article = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)
    if form.is_valid():
        article = form.save(commit=False)
        
        article.author = request.user
        article.save()

        messages.success(request,"Makale başarıyla güncellendi")
        return redirect("blog:dashboard")
    return render(request,"update.html",{"form":form})


@login_required(login_url = "user:login")
def deleteArticle(request,slug):
    article = get_object_or_404(Article,slug=slug)

    article.delete()

    messages.success(request,"Makale Başarıyla Silindi")

    return redirect("blog:dashboard")
def addComment(request,slug):
    post = get_object_or_404(Article, slug=slug)

    if request.method == "POST":
        author = request.POST.get("author")
        body = request.POST.get("body")

        newComment = Comment(author  = author, body = body)

        newComment.post = post

        newComment.save()
    return redirect(reverse("blog:detail",kwargs={"slug":slug}))