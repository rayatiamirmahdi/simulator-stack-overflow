from django.db import models
from django.contrib.auth.models import User

class Relations(models.Model):
    from_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    to_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_follow} follow {self.to_follow}"