from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django_summernote.fields import SummernoteTextField
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    img = models.FilePathField(path="./images")
    content = SummernoteTextField()
    pub_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("article-post", kwargs={"pk": str(self.id)})

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
    
class Comment(models.Model):
    post = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"