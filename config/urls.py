"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from graphene_django.views import GraphQLView

# раcкомментировать нужный вариант вьюхи для User
# from users.views import UserModelViewSet
from users.views import UserCustomViewSet
# from users.views import UserAPIView

from todo.views import ProjectModelViewSet, TodoModelViewSet

schema_view = get_schema_view(
    openapi.Info(
        title='ToDo for Projects',
        default_version='1.0',
        description='Documentation on project',
        license=openapi.License(name='MIT'),
        contact=openapi.Contact(email='megacunt@mail.ru')
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# в проде обычно используют SimpleRouter - без отображения точек входа API
# c DefaultRouter - тоже самое, но отображаются точки входа API (для отладки обычно)
router = DefaultRouter()

# раcкомментировать нужный вариант вьюхи для User
# router.register('users', UserModelViewSet)
router.register('users', UserCustomViewSet)

router.register('projects', ProjectModelViewSet)
router.register('todo', TodoModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth-token/', views.obtain_auth_token),
    path('api-jwt-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-jwt-token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/users/', UserAPIView.as_view()),
    path('api/', include(router.urls)),

    # добавляем точку входа для GraphQL, сразу включаем удобное отображение параметром
    # path('graphql/', GraphQLView.as_view(graphiql=True)),
    # для передачи post запросов извне (напр. через Postman) - нужно отключить контроль csrf-токена
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),

    # добавляем автодокументирование api с помощью Swagger, ReDoc
    # вариант с UI-интерфейсом
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # вариант без UI в вариантах с json, yaml. Переменная format будет определять формат выдачи
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-swagger-woui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # 1 вариант версионирования в URL
    # задаем эндпоинт для запроса пользователей с версией api (регуляркой задаем шаблон версии в виде "ЦИФРА.ЦИФРА")
    # преимущество - можно использовать для задания конкр. версий конкретным методам api
    # http://localhost:8000/api/users/
    # http://localhost:8000/api/2.0/users/
    # re_path(r'^api/(?P<version>\d\.\d)/users/$', UserCustomViewSet.as_view({'get': 'list'})),
    # path('api/<str:version>/users/', UserCustomViewSet.as_view({'get': 'list'})),

    # 2 вариант версионирования через пространство имён - позволяет разделить название в URL и версию в программе
    # path('api/2.0/', include((router.urls, 'users'), namespace='2.0')),
    # path('api/ver2/', include((router.urls, 'users'), namespace='2.0')),
]
