from django_filters import rest_framework as drf
from .models import Todo


class TodoFilter(drf.FilterSet):
    # используем фильтр по диапазону от и до для даты создания заметки
    created_at = drf.DateRangeFilter()

    class Meta:
        model = Todo
        # задаем поля, по которым будет доступна фильтрация
        fields = ['project', 'created_at']
