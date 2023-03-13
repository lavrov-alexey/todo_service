from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from todo.models import Project, Todo
from users.serializers import UserModelSerializer


class ProjectModelSerializer(ModelSerializer):
    # получаем в API строковое представление пользователей
    users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class TodoModelSerializer(ModelSerializer):
    # получаем развернутый связанный объект проекта, к кот. относится заметка
    # project = ProjectModelSerializer()
    project = serializers.StringRelatedField()
    creator = serializers.StringRelatedField()

    class Meta:
        model = Todo
        fields = '__all__'
