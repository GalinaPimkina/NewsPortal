from datetime import datetime, timedelta
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category
from newsportal import settings


@shared_task
def post_created(id):
    instance = Post.objects.get(id=id)

    subscriber_emails = []
    for cat in instance.category.all():
        subscriber_emails.append(User.objects.filter(subscriptions__category=cat).values_list('email', flat=True))

    subject = f'Новая статья в категории {instance.category}'

    text_content = (
        f'В ваших подписках появилась новая статья!\n\n'
        f'Заголовок: {instance.title}\n'
        f'Автор: {instance.author}\n\n'
        f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    html_content = (
        f'В ваших подписках появилась новая статья!<br><br>'
        f'Заголовок: {instance.title}<br>'
        f'Автор: {instance.author}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на статью</a>'
    )

    for email in subscriber_emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def new_posts_for_a_week():
    new_posts = Post.objects.filter(time_create__gte=datetime.now()-timedelta(days=7))
    categories = new_posts.values_list('category__category_name', flat=True)
    subscriptions = set(Category.objects.filter(category_name__in=categories).values_list('subscriptions__user__email', flat=True))
    html_content = render_to_string(template_name='daily_post.html', context={'posts': new_posts, 'link': settings.SITE_URL})

    msg = EmailMultiAlternatives(subject='Статьи за неделю', body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscriptions,)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()