from csv import DictReader
from datetime import date
from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import transaction
from django.utils.text import slugify


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("applications", nargs="*")

    def check_arguments_number(self, applications: list[str]) -> str:
        self.stdout.write(
            f"[*    ] Проверка количества переданных аргументов: {applications}"
        )

        if len(applications) == 1:
            return applications[0]
        else:
            raise CommandError("Необходимо передать один аргумент")

    def check_application_exists(self, application: str) -> None:
        self.stdout.write(f"[=*   ] Проверка существования приложения '{application}'")

        try:
            apps.get_app_config(application)
        except LookupError:
            raise CommandError("Приложение не найдено")

    def check_model_exists(self, application: str) -> Any:
        self.stdout.write(
            f"[==*  ] Проверка существования модели 'Phone' в '{application}'"
        )

        try:
            return apps.get_model(application, "Phone")
        except LookupError:
            raise CommandError("Модель не найдена")

    def import_phones(self, phones: Any) -> Any:
        try:
            with transaction.atomic():
                self.stdout.write("[===* ] Удаление текущих данных")
                phones.objects.all().delete()

                self.stdout.write("[====*] Импорт новых данных")
                with open("apps/django/hw3/phones.csv", encoding="utf-8") as file:
                    reader = DictReader(file, delimiter=";")
                    for row in reader:
                        phones.objects.create(
                            name=row["name"],
                            slug=slugify(row["name"]),
                            release_date=date.fromisoformat(row["release_date"]),
                            price=int(row["price"]),
                            image=row["image"],
                            lte_exists=row["lte_exists"] == "True",
                        )
            self.stdout.write("[=====] Готово")
        except Exception as e:
            raise CommandError(e)

    def handle(self, *args: Any, **options: Any) -> None:
        applications: list[str] = options["applications"]
        application = self.check_arguments_number(applications)
        self.check_application_exists(application)
        phones = self.check_model_exists(application)
        self.import_phones(phones)
