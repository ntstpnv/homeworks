from django.conf import settings

from server.common import views
from . import models


class MenuView(views.MenuView):
    queryset = [
        settings.LINK("Показать инфоцыганские курсы", "courses"),
        settings.LINK("Показать новостные статьи", "articles"),
    ]

    back = "django"


class CourseView(views.MenuView):
    template_name = "hw4/courses.html"
    queryset = models.DBManager.get_courses()

    title = "Инфоцыганские курсы"
    back = "hw4"

    def get(self, request, *args, **kwargs):
        if "generate" in request.GET:
            models.DBManager().generate()
        return super().get(request, *args, **kwargs)


class ArticleView(views.MenuView):
    template_name = "hw4/news.html"
    queryset = models.DBManager.get_articles()

    back = "hw4"
