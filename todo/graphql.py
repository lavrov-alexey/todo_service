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
    # команда получения пользователей по заданным фамилии и/или имени (фильтрация) - необяз. параметры
    get_user_by_name = graphene.List(UserObjectType,  # возвращаемый тип - список пользователей графена
                                     first_name=graphene.String(required=False),  # тип - строка графена
                                     last_name=graphene.String(required=False)  # тип - строка графена
                                     )

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
        # запрос по конкретному пользователю с получением сразу по нему списков его заметок и проектов, куда он допущен
        # для связей 1 ко многим и многие ко многим - в django автоматом создается поле Somename_Set
        # вот так можно вернуть все проекты (все их поля), к которым есть доступ у конкретного запрошенного пользователя
        # return User.objects.get(pk=pk).project_set.all()

    # функция для фильтрации пользователей по переданным имени и/или фамилии
    def resolve_get_user_by_name(self, info, first_name=None, last_name=None):
        fio_dict = {}
        if first_name:
            # добавив __contains - делаем станд. фильтрацию Джанго по подстроке
            fio_dict['first_name__contains'] = first_name
        if last_name:
            fio_dict['last_name__contains'] = last_name
        if fio_dict:
            return User.objects.filter(**fio_dict)
        # если не переданы - отдаем полный список
        return User.objects.all()

# class Query(graphene.ObjectType):  # первичная тренировка
#     # описываем в схеме команду и какой тип данных будет возвращен
#     hello = graphene.String()
#     # описываем собственно саму команду - начинается с "resolve_" и имени команды
#     def resolve_hello(self, info):
#         return 'world'

# Все операции на создание, изменение, удаление - в графене это мутации
class ProjectCreateMutation(graphene.Mutation):
    # класс Arguments - для описания входных параметров
    class Arguments:
        # входные параметры
        name = graphene.String(required=True)
        repo_link = graphene.String(required=True)
        # users = graphene.List(UserObjectType)
        is_deleted = graphene.Boolean(required=True)

    # возвращаемый параметр
    project = graphene.Field(ProjectObjectType)

    @classmethod  # метод изменения оформляется как класс-метод, отдаем входные параметры
    def mutate(cls, root, info, name, repo_link='', is_deleted=False):
    # def mutate(cls, root, info, name, repo_link, users, is_deleted=False):
        # подставляем вх. параметры в модель Джанго и сохраняем
        project = Project(name=name, repo_link=repo_link, is_deleted=is_deleted)
        # project = Project(name=name, repo_link=repo_link, users=users, is_deleted=is_deleted)
        project.save()
        return cls(project)


# создаем класс с мутациями
class Mutatitions(graphene.ObjectType):
    create_project = ProjectCreateMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutatitions)
