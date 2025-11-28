from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    POST_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    media_url = models.URLField(blank=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}"

    class Meta:
        db_table = 'feed_post'
        ordering = ['-created_at']

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

    class Meta:
        db_table = 'feed_like'
        unique_together = ('user', 'post')

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.post.id}"

    class Meta:
        db_table = 'feed_save'
        unique_together = ('user', 'post')