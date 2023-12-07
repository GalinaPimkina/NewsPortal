from django.urls import path, include
from .views import *


urlpatterns = [
    path('pages/', include('django.contrib.flatpages.urls')),

    path('', PostList.as_view(), name='news'),
    path('<int:pk>', PostText.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions',),
]
