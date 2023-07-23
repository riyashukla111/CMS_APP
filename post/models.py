from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True) # lets assume title to be unique field, it may can vary.
    description = models.CharField(max_length=500)
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.post_id.title + '-' + self.user_id.username 