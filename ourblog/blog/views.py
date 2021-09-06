from django.shortcuts import render,redirect,get_object_or_404
from .forms import CommentForm, ArticleForm, UserUpdateForm, ProfileUpdateForm
from .models import Article, Comment, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import Count,Q
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.views.generic import CreateView, DetailView
import random


class AddCategoryView(CreateView):
    model = Category
    template_name = 'addCategory.html'
    fields = '__all__'

def CategoryView(request, category):
    category_post = Article.objects.filter(category=category)
    return render(request, 'categories.html', {'category':category, 'category_post':category_post})

def articles(request, slug=None, tag_slug=None):
    articles = Article.objects.all()
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    tag=None
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        articles = Article.objects.filter(tags__in=[tag])

    query = request.GET.get("q")
    if query:
        articles=Article.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()

    context = {
        "articles": articles,
        "tag":tag,
        "page":page,
        }
    
    return render(request,"articles.html", context)   


def LikeView(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.likes.add(request.user)
    return redirect('blog:detail', article.slug)

def about(request):
    return render(request,"about.html")

@login_required(login_url = "accounts:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)


@login_required(login_url = "allauth:account_login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    common_tags = Article.tags.most_common()[:4]
    if form.is_valid():
        article = form.save(commit=False)
        article.slug = slugify(article.title)
        article.author = request.user
        article.save()
        form.save_m2m()

        messages.success(request,"Article created successfully")
        return redirect("blog:dashboard")
    context = {
        'common_tags':common_tags,
        'form':form,
    }
    return render(request,"addarticle.html",context)

class ArticleDetail(DetailView):
    model = Article
    context_object_name = "article"
    template_name = "post_detail.html"
def detail(request,post):
    #article = Article.objects.filter(id = id).first()   
    article = get_object_or_404(Article, slug=post)
    # all_article = list(Article.objects.exclude(slug=post))
    # comments = article.comments.all()
    article_tags= Article.tags.values_list('id', flat=True)
    similar_posts = Article.objects.filter(tags__in=article_tags).exclude(id=article.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-pub_date')[:3]
    comments = article.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = article
            new_comment.save()
            return redirect(article.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()
    context = {
        "article":article,
        "comments":comments,
        "comment_form":comment_form, 
        "similar_posts":similar_posts 
    }

    return render(request,"detail.html",context)


@login_required(login_url = "allauth:account_login")
def updateArticle(request, slug):

    article = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)
    if form.is_valid():
        article = form.save(commit=False)
        
        article.author = request.user
        article.save()

        messages.success(request,"Article has been Updated")
        return redirect("blog:dashboard")
    return render(request,"update.html",{"form":form})


@login_required(login_url = "allauth:account_login")
def deleteArticle(request,slug):
    article = get_object_or_404(Article,slug=slug)

    article.delete()

    messages.success(request,"Article Deleted Successfully")

    return redirect("blog:dashboard")
# def addComment(request,slug):
#     post = get_object_or_404(Article, slug=slug)
#     comments = post.comments.filter(active=True)
#     new_comment = None
    
    
#     if request.method == "POST":
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#             return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
#     else:
#         comment_form = CommentForm()

def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)
        
        # print(form)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            article_url = request.POST.get('article_url')  # from hidden input

            print(post_id)
            print(parent_id)
            print(article_url)


            reply = form.save(commit=False)
    
            reply.post = Article(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(article_url+'#'+str(reply.id))

    return redirect("/")

def tagged(request, tags):
    # tag = get_object_or_404(Tag, slug=slug)
    posts = Article.objects.filter(tags=tags)
    return render(request, 'articles.html', {'tags':tags, 'posts':posts})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('blog:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


