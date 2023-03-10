from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets

from .serializers import UserModelSerializer
from .models import User

# Если нужно обработать запросы в функции - делать через декоратор, в кот. указать запросы
# @api_view(['GET', 'POST'])
# Если нужно отобразить - использовать декоратор с указанием используемого рендера
# @renderer_classes([JSONRenderer])
# def test_function(request):
#     pass

# вариант для полного набора методов на базе ModelViewSet
# class UserModelViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserModelSerializer

# вариант части методов (GET, UPDATE) на базе Custom ViewSet
class UserCustomViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
