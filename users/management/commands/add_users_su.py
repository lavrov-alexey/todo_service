from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "If don't exists, create superuser and few test's users"

    def handle(self, *args, **options):
        call_command('loaddata', 'test_users')
        return f'Вызвана команда add_users_su.\n' \
               f'Добавлены суперпользователь "AUTO_SU" и пользователи "test1"-"test3" из фикстуры test_users.json\n' \
               f'Пароль для всех добавленных пользователей слово "пароль" в англ. раскладке + "1234": gfhjkm1234'
