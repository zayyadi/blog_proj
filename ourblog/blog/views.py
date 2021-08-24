from django.shortcuts import render,redirect,get_object_or_404
from .forms import CommentForm, ArticleForm, UserUpdateForm, ProfileUpdateForm
from .models import Article, Comment, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.views.generic import CreateView
import random


class AddCategoryView(CreateView):
    model = Category
    template_name = 'addCategory.html'
    fields = '__all__'

def CategoryView(request, category):
    category_post = Article.objects.filter(category=category)
    return render(request, 'categories.html', {'category':category, 'category_post':category_post})

def articles(request, slug=None, tag_slug=None):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    tag=None
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    all_articles = list(Article.objects.all())
    recent_articles = random.sample(all_articles, 3)
    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        articles = Article.objects.filter(tags__in=[tag])

    context = {
        "articles": articles,
        "tag":tag,
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


def detail(request,slug):
    #article = Article.objects.filter(id = id).first()   
    article = get_object_or_404(Article, slug=slug)
    all_article = list(Article.objects.exclude(slug=slug))
    comments = article.comments.all()
    like_article = random.sample(all_article, 3)

    article_tags= Article.tags.values_list('slug', flat=True)
    similar_posts = Article.objects.filter(tags__in=article_tags).exclude(slug=article.slug)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-pub_date')[:3]

    context = {
        "article":article,
        "comments":comments, 
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

    messages.success(request,"Makale Başarıyla Silindi")

    return redirect("blog:dashboard")
def addComment(request,slug):
    post = get_object_or_404(Article, slug=slug)
    
    
    if request.method == "POST":
        
        body = request.POST.get("body")

        newComment = Comment( body=body)

        newComment.post = post

        newComment.save()
    return redirect(reverse("blog:detail",kwargs={"slug":slug}))

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
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


