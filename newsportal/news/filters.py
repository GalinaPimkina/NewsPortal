from django_filters import FilterSet, DateTimeFilter, ModelMultipleChoiceFilter, CharFilter
from django.forms import DateTimeInput
from .models import *


class PostFilter(FilterSet):
    add_after = DateTimeFilter(
        field_name='time_create',
        lookup_expr='gte',
        label='Опубликовано после ',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
                ),
        )
    category = ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        conjoined=True,
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }