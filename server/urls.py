from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

from server.common import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        views.MenuView.as_view(
            queryset=settings.GROUPS,
            title="Выберите модуль",
        ),
        name="home",
    ),
    *[
        path(
            f"{group}/",
            views.MenuView.as_view(
                queryset=settings.APPS[group],
                title="Выберите тему",
                back="home",
            ),
            name=group,
        )
        for group in settings.APPS
    ],
    *[
        path(f"{group}/{link.path}/", include(f"server.apps.{group}.{link.path}.urls"))
        for group, apps in settings.APPS.items()
        for link in apps
    ],
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *(debug_toolbar_urls() if settings.DEBUG else []),
]
