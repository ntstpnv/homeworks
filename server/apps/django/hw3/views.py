from django.conf import settings
from django.shortcuts import redirect

from server.common import views
from . import models


class MenuView(views.MenuView):
    queryset = [
        settings.LINK("Показать каталог смартфонов", "phones"),
    ]

    back = "django"


class PhoneListView(views.MenuView):
    template_name = "hw3/phones.html"

    title = "Каталог смартфонов"
    back = "hw3"

    def get(self, request, *args, **kwargs):
        request.session["sort"] = request.GET.get("sort", "name")

        return (
            super().get(request, *args, **kwargs)
            if request.GET.get("sort")
            else redirect(f"{request.path}?sort=name")
        )

    def get_queryset(self):
        return models.Phone.objects.all().order_by(self.request.GET.get("sort"))


class PhoneView(views.BaseDetailView):
    template_name = "hw3/phone.html"

    back = "phones"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "title": self.object.name,
            "sort": self.request.session.get("sort"),
        }

    def get_object(self, queryset=None):
        return models.Phone.objects.get(slug=self.kwargs.get("slug"))
