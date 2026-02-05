from django.urls import path

from . import views


urlpatterns = [
    path("", views.MenuView.as_view(), name="hw3"),
    path("catalog/", views.PhoneListView.as_view(), name="phones"),
    path("catalog/<slug:slug>/", views.PhoneView.as_view(), name="phone"),
]
