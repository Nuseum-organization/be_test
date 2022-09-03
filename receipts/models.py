from django.db import models
from posts.models import Post

class Receipt(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  image = models.CharField(max_length=250, blank=True)

  def __str__(self):
    return f'[post_no.{self.post.id}] {self.image} :: {self.id}'
