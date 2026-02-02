from os import listdir

from django.conf import settings

from apps.common import views


class MenuView(views.MenuView):
    queryset = [
        settings.LINK("Показать текущее время", "current_time"),
        settings.LINK("Показать рабочую директорию", "workdir"),
    ]

    title = "Выберите задание"
    back = "django"


class CurrentTimeView(views.BaseTemplateView):
    template_name = "hw1/current_time.html"

    title = "Текущее время"
    back = "hw1"


class WorkdirView(views.MenuView):
    template_name = "hw1/workdir.html"
    queryset = listdir()

    title = "Рабочая директория"
    back = "hw1"
