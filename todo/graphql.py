import graphene
from graphene_django import DjangoObjectType

from .models import Project, Todo
from users.models import User


# связываем объекты графена с моделями из Джанго (по сути - некий сериализатор,
# позволяющий получить из одного представления другое)
class ProjectObjectType(DjangoObjectType):
    class Meta:
        model = Project  # указываем модель из Джанги
        fields = '__all__'  # и список нужных полей из модели


class TodoObjectType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = '__all__'


class Query(graphene.ObjectType):
    # описываем в схеме команду и какой тип данных будет возвращен (список определенных нами объектов проектов)
    all_projects = graphene.List(ProjectObjectType)
    all_todo = graphene.List(TodoObjectType)

    # описываем собственно саму команду - начинается с "resolve_" и имени команды
    def resolve_all_projects(self, info):
        return Project.objects.all()

    def resolve_all_todo(self, info):
        return Todo.objects.all()

# class Query(graphene.ObjectType):  # первичная тренировка
#     # описываем в схеме команду и какой тип данных будет возвращен
#     hello = graphene.String()
#     # описываем собственно саму команду - начинается с "resolve_" и имени команды
#     def resolve_hello(self, info):
#         return 'world'

schema = graphene.Schema(query=Query)