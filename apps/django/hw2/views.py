from django.conf import settings
from django.shortcuts import redirect

from apps.common import views
from . import models


class MenuView(views.MenuView):
    queryset = [
        settings.LINK("Показать кулинарные рецепты", "recipes"),
    ]

    back = "django"


class RecipeListView(views.MenuView):
    template_name = "hw2/recipes.html"
    model = models.Dish
    paginate_by = 3

    title = "Кулинарные рецепты"
    back = "hw2"

    def get(self, request, *args, **kwargs):
        request.session["page"] = request.GET.get("page", "1")

        return (
            super().get(request, *args, **kwargs)
            if request.GET.get("page")
            else redirect(f"{request.path}?page=1")
        )


class RecipeView(views.BaseDetailView):
    template_name = "hw2/recipe.html"
    queryset = models.Dish.objects.prefetch_related("recipe__ingredient__unit")

    back = "recipes"

    def get(self, request, *args, **kwargs):
        return (
            super().get(request, *args, **kwargs)
            if request.GET.get("servings")
            else redirect(f"{request.path}?servings=1")
        )

    def get_context_data(self, **kwargs):
        servings = int(self.request.GET.get("servings"))

        return {
            **super().get_context_data(**kwargs),
            "title": self.object.name,
            "objects": [
                f"{dish.ingredient.name} - {dish.amount * servings} {dish.ingredient.unit.name}"
                for dish in self.object.recipe.all()
            ],
            "page": self.request.session.get("page"),
        }
