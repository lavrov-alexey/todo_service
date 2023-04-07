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
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# раcкомментировать нужный вариант вьюхи для User
# from users.views import UserModelViewSet
from users.views import UserCustomViewSet
# from users.views import UserAPIView

from todo.views import ProjectModelViewSet, TodoModelViewSet

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
    # задаем эндпоинт для запроса пользователей с версией api
    # http://localhost:8000/api/users/
    # http://localhost:8000/api/2.0/users/
    re_path(r'^api/(?P<version>\d\.\d)/users/$', UserCustomViewSet.as_view({'get': 'list'})),
    path('api/', include(router.urls)),
]
