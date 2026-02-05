from django.urls import path

from . import views

urlpatterns = [
    path("", views.MenuView.as_view(), name="hw4"),
    path("courses/", views.CourseView.as_view(), name="courses"),
    path("articles/", views.ArticleView.as_view(), name="articles"),
]
