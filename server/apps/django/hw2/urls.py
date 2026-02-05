from django.urls import path

from . import views


urlpatterns = [
    path("", views.MenuView.as_view(), name="hw2"),
    path("recipes/", views.RecipeListView.as_view(), name="recipes"),
    path("recipes/<slug:slug>/", views.RecipeView.as_view(), name="recipe"),
]
