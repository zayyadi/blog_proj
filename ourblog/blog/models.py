from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager
from PIL import Image
from django.urls import reverse
import os


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'article_pics'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    content = SummernoteTextField()
    image = models.ImageField(default='default.jpg', upload_to=path_and_rename)
    pub_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    category = models.CharField(max_length=255,default='uncategorized')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    snippet = models.CharField(max_length=255)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog:detail",args=[self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

       

class Comment(models.Model):
    post = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    author = models.ManyToManyField(User, related_name="authors")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    email = models.EmailField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']
    
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

    def __str__(self):
        return f"Comment {self.body} by {self.author}"

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:articles')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

