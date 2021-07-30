from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager
from user.models import Profile


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    image = models.FileField(blank = True,null = True)
    content = SummernoteTextField()
    pub_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes')

    def number_of_likes(self):
        return self.likes.all().count()

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("article-post", kwargs={"pk": str(self.id)})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    author = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.author}"

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"