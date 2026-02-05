from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(r"api/measurements", views.MeasurementViewSet, basename="measurement")
router.register(r"api/sensors", views.SensorViewSet, basename="sensor")

urlpatterns = [
    path("", views.MenuView.as_view(), name="hw5"),
    *router.urls,
]
