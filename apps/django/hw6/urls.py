from django.urls import path
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r"api/warehouses", views.WarehouseViewSet, basename="warehouse")
router.register(r"api/items", views.ItemViewSet, basename="item")

urlpatterns = [
    path("", views.MenuView.as_view(), name="hw6"),
    *router.urls,
]
