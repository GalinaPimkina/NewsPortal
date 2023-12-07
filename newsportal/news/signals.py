from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from news.tasks import post_created

@receiver(post_save, sender=Post)
def notify_subscribers(instance, **kwargs):
    """
    сигнал срабатывает после сохранения нового поста, активируя задачу post_created

    """
    post_created.delay(instance.id)