import shutil
import pathlib

from django.core.management import call_command
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("arg_list", nargs="*")

    def success_msg(self, msg: str) -> None:
        self.stdout.write(f"ОК. {msg}")

    def check_args_number(self, args: list[str]) -> str:
        if len(args) != 1:
            raise CommandError("Необходимо передать один аргумент")

        arg = args[0]
        self.success_msg(f"Передан один аргумент - '{arg}'")
        return arg

    def check_app_exists(self, app: str) -> str:
        try:
            path = apps.get_app_config(app).path
            self.success_msg(f"Приложение '{app}' найдено")
            return path

        except LookupError:
            raise CommandError(f"Приложение '{app}' не найдено")

    def find_tables(self, app: str) -> list[str]:
        tables = [
            table
            for table in connection.introspection.table_names()
            if table.startswith(app)
        ]

        self.success_msg(f"Найденные таблицы: {tables}")
        return tables

    def drop_tables(self, tables: list[str]) -> None:
        if tables:
            with connection.cursor() as cursor:
                for table in tables:
                    cursor.execute(f"DROP TABLE {table} CASCADE")
                    self.success_msg(f"Таблица '{table}' удалена")

    def clear_migrations(self, app: str) -> None:
        MigrationRecorder(connection).migration_qs.filter(app=app).delete()
        self.success_msg("Записи миграций в БД удалены")

    def delete_dir(self, path: str) -> None:
        try:
            shutil.rmtree(pathlib.Path(path) / "migrations")
            self.success_msg("Папка с миграциями удалена")

        except FileNotFoundError:
            self.success_msg("Папка с миграциями не найдена")

        except Exception as e:
            raise CommandError(e)

    def make_migrations(self, app: str) -> None:
        call_command("makemigrations", app)
        call_command("migrate", app)
        self.success_msg(f"Данные для '{app}' обновлены")

    def handle(self, *args, **options):
        arg_list = options["arg_list"]
        app = self.check_args_number(arg_list)
        path = self.check_app_exists(app)
        tables = self.find_tables(app)
        self.drop_tables(tables)
        self.clear_migrations(app)
        self.delete_dir(path)
        self.make_migrations(app)
