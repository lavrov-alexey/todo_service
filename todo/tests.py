from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
from rest_framework import status
from mixer.backend.django import mixer
from .views import ProjectModelViewSet
from users.models import User
from todo.models import Project, Todo

# Базовый тест (нижний уровень) на основе тестов Джанго.
# Тестирует вью, сериализаторы и модели. Урлы - не тестирует, т.к. реквест пихаем напрямую во вью
class ProjectTestCase(TestCase):

    # метод будет вызываться перед запуском теста
    def setUp(self) -> None:
        # для того, чтобы авторизоваться в запросе - создадим суперпользователя и пр. данные
        self.user = User.objects.create_superuser(username='testSU', password='qwerty1234', email='testSU@mail.ru')
        self.project = Project.objects.create(name='Project Test')
        # self.todo = Todo.objects.create(project=self.project, todo_text='Test ToDo text', creator=self.user)
        # print(f'{self.user=}\n{self.project=}\n{self.todo=}')

    # метод будет вызываться после выполнения теста
    def tearDown(self) -> None:
        pass

    # все методы, начинающиеся на test... будут интерпретироваться как тесты и соотв. образом отображаться
    def test_anonim_get_project_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        view = ProjectModelViewSet.as_view({'get': 'list'})
        response = view(request)
        # ловим ошибку доступа по неавторизованному запросу (не залогинены)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_get_project_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        force_authenticate(request, user=self.user)
        view = ProjectModelViewSet.as_view({'get': 'list'})
        response = view(request)
        # по авторизованному пользователю - запрос проходит и ответ не пустой
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        # в ответе будет пусто, если мы для тестов не создадим данные сами (для тестов не используется обычная база)
        # print(response.data)

# Тест след. уровня - уже на базе полноценного api-клиента
# Тестирует урл (endpoint), вью, сериализаторы и модели.
# Путем эмуляции непосредственно api-запросов, создает сам api-клиента self.client
class TodoClientTestCase(APITestCase):

    # метод будет вызываться перед запуском теста
    def setUp(self) -> None:
        # для того, чтобы авторизоваться в запросе - создадим суперпользователя и пр. данные
        self.user = User.objects.create_superuser(username='testSU', password='qwerty1234', email='testSU@mail.ru')
        # self.project = Project.objects.create(name='Project Test')
        # исп. Миксер, чтобы сгенерить поля по модели автом., часть полей - можно вручную, связанные модели
        self.project = mixer.blend(Project)
        # self.todo = Todo.objects.create(project=self.project, todo_text='Test ToDo text', creator=self.user)
        self.todo = mixer.blend(Todo, todo_text='Special concrete text', project__repo_link='test mixer custom link')

    def test_anonim_get_todo_list(self):
        # создаем и направляем полноценный api-запрос
        response = self.client.get('/api/todo/')
        # ловим ошибку доступа по неавторизованному запросу (не залогинены)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_get_todo_list(self):
        # аутентифицируем нашего тестового api-клиента созданным нами пользователем
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/todo/')
        # по авторизованному пользователю - запрос проходит и ответ не пустой
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # тест сценария - клиент логинится, получает todo, разлогинивается и получает ошибку доступа
    def test_login_logout_get_todo_list(self):
        # либо можем передать логин, пароль и просто залогинить пользователя
        self.client.login(username='testSU', password='qwerty1234')
        response = self.client.get('/api/todo/')
        # по авторизованному пользователю - запрос проходит и ответ не пустой
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        # теперь разлогиниваемся и проверяем, что ответ будет уже 403
        self.client.logout()
        response = self.client.get('/api/todo/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # тест создания заметки
    def test_post_todo(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/todo/', {"todo_text": "ToDo test POST text", "project": 1, "creator": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # получаем созданную заметку и проверяем, что создалось именно то, что нужно
        new_todo_id = response.data.get('id')
        new_todo = Todo.objects.get(pk=new_todo_id)
        self.assertEqual(new_todo.todo_text, 'ToDo test POST text')
