from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager
from PIL import Image
from django.urls import reverse


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    content = SummernoteTextField()
    pub_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    category = models.CharField(max_length=255,default='blogs')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def total_likes(self):
        return self.likes.count()

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
    author = models.ManyToManyField(User, related_name="authors")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

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


# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, related_name='replies',  on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     reply = models.TextField()

#     def __str__(self):
#         return self.user.username

#     @property
#     def get_replies(self):
#         return self.replies.all()
