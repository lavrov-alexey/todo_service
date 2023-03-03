from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet

from .serializers import UserModelSerializer
from .models import User


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


# Если нужно обработать запросы в функции - делать через декоратор, в кот. указать запросы
# @api_view(['GET', 'POST'])
# Если нужно отобразить - использовать декоратор с указанием используемого рендера
# @renderer_classes([JSONRenderer])
# def test_function(request):
#     pass
