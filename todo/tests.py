from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import ProjectModelViewSet

# Базовый тест (нижний уровень) на основе тестов Джанго
class ProjectTestCase(TestCase):

    # все методы, начинающиеся на test... будут интерпретироваться как тесты и соотв. образом отображаться
    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        view = ProjectModelViewSet.as_view({'get': 'list'})
        response = view(request)
        # ловим ошибку доступа по неавторизованному запросу (не залогинены)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
