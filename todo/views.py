from rest_framework import status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.renderers import JSONRenderer, AdminRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, \
    BasePermission, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
    # включает интеграцию моделей разрешений Django DRF, все авторизованные - могут читать

from todo.filters import TodoFilter
from todo.models import Project, Todo
from todo.serializers import ProjectModelSerializer, TodoModelSerializer


# На основе базового класса - можно создавать свои классы разрешений, переопред. метод has_permission
# DjangoModelPermissions - интеграция моделей разрешений Django и DRF, все авторизованные пользователи - могут читать
# DjangoModelPermissionsOrAnonReadOnly - все неавториз. пользователи могут читать
class CustomPermissions(BasePermission):
    def has_permission(self, request, view):
        # Должен возвращать bool, напр. если есть юзер и у него задано имя
        return request.user and request.username


# class ProjectPagination(PageNumberPagination):
#     PAGE_SIZE = 10


class ProjectModelViewSet(ModelViewSet):
    # Можем переопределить рендер для конкретного класса - например - отображение в чистом JSON
    # renderer_classes = [JSONRenderer]
    # renderer_classes = [AdminRenderer]
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    # pagination_class = ProjectPagination

    def get_queryset(self):
        queryset = Project.objects.all()
        # вытаскиваем из запроса переданное значение в параметре name
        name = self.request.query_params.get('name', None)
        # если параметр не передавалася - просто отдаем данные по всем проектам
        if name:
            # если передавалась в пар-рах подстрока для поиска - отфильтровываем из выборки
            queryset = queryset.filter(name__contains=name)
        return queryset


# class TodoPagination(PageNumberPagination):
#     PAGE_SIZE = 20


class TodoModelViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoModelSerializer
    # pagination_class = TodoPagination
    filterset_class = TodoFilter

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.save()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
