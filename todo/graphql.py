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


class UserObjectType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class Query(graphene.ObjectType):
    # описываем в схеме команду и в 1ом параметре - передать какой тип данных будет возвращен
    # (напр. список определенных нами объектов проектов)
    all_projects = graphene.List(ProjectObjectType)
    all_todo = graphene.List(TodoObjectType)
    all_users = graphene.List(UserObjectType)
    # для получ. по id - нужно передать тип возвращаемых данных и входные - этот id и указываем, что это обяз. параметр
    get_project_by_id = graphene.Field(ProjectObjectType, pk=graphene.Int(required=True))
    get_user_by_id = graphene.Field(UserObjectType, pk=graphene.Int(required=True))

    # описываем собственно саму команду - начинается с "resolve_" и имени команды
    def resolve_all_projects(self, info):
        return Project.objects.all()

    def resolve_all_todo(self, info):
        return Todo.objects.all()

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_get_project_by_id(self, info, pk):
        return Project.objects.get(pk=pk)

    def resolve_get_user_by_id(self, info, pk):
        return User.objects.get(pk=pk)

# class Query(graphene.ObjectType):  # первичная тренировка
#     # описываем в схеме команду и какой тип данных будет возвращен
#     hello = graphene.String()
#     # описываем собственно саму команду - начинается с "resolve_" и имени команды
#     def resolve_hello(self, info):
#         return 'world'

schema = graphene.Schema(query=Query)