from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    slug = models.SlugField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create']

    def __str__(self):
        return f"{self.slug} ---user {self.user}"

    def get_absolute_url(self):
        return reverse("home:detail_url", args=(self.id, self.slug))
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_co")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_co")
    body = models.CharField(max_length=200)
    reply = models.ForeignKey("Comment", on_delete=models.CASCADE , related_name="reply_co", null=True, blank=True )
    is_reply = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} comment for this {self.post}"






