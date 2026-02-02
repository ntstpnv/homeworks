import pathlib
import shutil

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


APPS = [link.path for link in settings.APPS["django"]]


class Command(BaseCommand):
    def handle(self, *args, **options):
        paths = [apps.get_app_config(app).path for app in APPS]
        self.stdout.write("Все приложения найдены")

        tables = [
            table
            for app in APPS
            for table in connection.introspection.table_names()
            if table.startswith(app)
        ]
        self.stdout.write("Все таблицы найдены")

        if tables:
            with connection.cursor() as cursor:
                for table in tables:
                    cursor.execute(f"DROP TABLE {table} CASCADE")
        self.stdout.write("Все таблицы удалены")

        for app in APPS:
            MigrationRecorder(connection).migration_qs.filter(app=app).delete()
        self.stdout.write("Все записи миграций удалены")

        for path in paths:
            try:
                shutil.rmtree(pathlib.Path(path) / "migrations")
            except FileNotFoundError:
                pass
        self.stdout.write("Все папки с миграциями удалены")

        for app in APPS:
            try:
                call_command("makemigrations", app)
                call_command("migrate", app)
            except CommandError:
                pass
        self.stdout.write("Готово")
