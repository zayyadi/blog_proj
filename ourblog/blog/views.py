from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .forms import CommentForm, ArticleForm
from .models import Article, Comment, Like
from user.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from taggit.models import Tag


def articles(request, slug=None):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    articles = Article.objects.all()
    paginate_by = 5
    
    return render(request,"articles.html", {"articles": articles})
    
    

# def view_comment(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#     comments = article.comments.all()
#     common_tags = Article.tags.most_common()[:4]
    
#     return render(request,"articles.html",{"article": article, "comments": comments, "common_tags": common_tags})
    

    
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

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Article.tags.most_common()[:4]
    posts = Article.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'common_tags':common_tags,
        'posts':posts,
    }
    return render(request, 'articles.html', context)



def BlogPostLike(request, slug):
    user = request.user
    if request.method == 'POST':
        article = Article.objects.get(slug=slug)
        profile = Profile.objects.get(user=user)

        if profile in article.liked.all():
            article.liked.remove(profile)
        else:
            article.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, slug=slug)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            article.save()
            like.save()
    return redirect('blog:detail')