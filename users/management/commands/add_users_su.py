from django.core.management import BaseCommand, call_command
from users.models import User


class Command(BaseCommand):
    help = "Если тест. пользователей и супер-пользователя нет - создаст их"

    # Вариант-1. Создание пользователей через фикстуры
    # def handle(self, *args, **options):
    #     call_command('loaddata', 'test_users')
    #     return f'Вызвана команда add_users_su.\n' \
    #            f'Добавлены суперпользователь "AUT O_SU" и пользователи "test1"-"test3" из фикстуры test_users.json\n' \
    #            f'Пароль для всех добавленных пользователей слово "пароль" в англ. раскладке + "1234": gfhjkm1234'


    # Вариант-2. Создание через команды
    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        # удаляем всех пользователей
        User.objects.all().delete()
        user_count = options['count']

        # создаем суперпользователя
        User.objects.create_superuser('AUTO_SU', 'su@su.gov', 'gfhjkm1234')

        # создаем тестовых пользователей
        for idx in range(1, user_count + 1):
            User.objects.create_user(f'test{idx}', f'test{idx}@mail.ru', 'gfhjkm1234')

        return f'Вызвана команда add_users_su.\n' \
               f'Добавлены суперпользователь "AUTO_SU" и пользователи "test1"-"testN",\n' \
               f'где N - опц. параметр команды\n' \
               f'Пароль для всех добавленных пользователей слово "пароль" в англ. раскладке + "1234": gfhjkm1234'