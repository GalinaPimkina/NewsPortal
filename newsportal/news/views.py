from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .filters import *
from .forms import *
from .models import *


class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    extra_context = {'title': 'Все новости'}


class PostText(DetailView):
    model = Post
    template_name = 'posttext.html'
    context_object_name = 'posttext'
    extra_context = {'title': 'Подробнее...'}


class PostSearch(ListView):
    model = Post
    template_name = 'postsearch.html'
    context_object_name = 'postsearch'
    paginate_by = 5
    extra_context = {'title': 'Поиск'}
    ordering = '-time_create'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = CreatePostForm
    model = Post
    template_name = 'post_edit.html'
    extra_context = {'title': 'Создание новой записи'}


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = CreatePostForm
    model = Post
    template_name = 'post_edit.html'
    extra_context = {'title': 'Редактирование записи'}


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    extra_context = {'title': 'Удаление записи'}


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriptions.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriptions.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(Subscriptions.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(request, 'subscriptions.html', {'title': 'Подписки', 'categories': categories_with_subscriptions},)




