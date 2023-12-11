from django.core.cache import cache
from django.db import models
from django.contrib.auth.admin import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse, reverse_lazy


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(post_rating=Coalesce(Sum('post_rating'), 0))['post_rating']
        author_comments_rating = Comment.objects.filter(user_id=self.user).aggregate(comment_rating=Coalesce(Sum('comment_rating'), 0))['comment_rating']
        author_posts_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(post_comment_rating=Coalesce(Sum('comment_rating'), 0))['post_comment_rating']

        self.user_rating = author_posts_rating * 3 + author_comments_rating + author_posts_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.category_name}"

    class Meta:
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    NEWS = 'news'
    POST = 'post'

    POST_CHOICE = [
        (NEWS, 'Новость'),
        (POST, 'Статья')
    ]
    post_category = models.CharField(max_length=4, choices=POST_CHOICE, default=POST)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', null=True)
    title = models.CharField(max_length=64)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[0:123]} ..."

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')

    class Meta:
        verbose_name_plural = 'Статьи и новости'


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscriptions(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions',)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions',)


