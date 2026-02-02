from django.conf import settings
from rest_framework import mixins, viewsets


from apps.common import views
from . import serializers, models


class MenuView(views.MenuView):
    template_name = "hw5/sensors.html"

    title = "Температурные датчики"
    back = "django"

    def get_queryset(self):
        return [
            settings.LINK("Создать измерение", "measurement-list"),
            settings.LINK("Создать датчик", "sensor-list"),
            settings.LINK("Показать датчики", "sensor-list"),
            *list(models.Sensor.objects.all()),
        ]


class SensorViewSet(viewsets.ModelViewSet):
    back = "hw5"

    def get_queryset(self):
        return (
            models.Sensor.objects.prefetch_related("measurements")
            if self.action == "retrieve"
            else models.Sensor.objects.all()
        )

    def get_serializer_class(self):
        return (
            serializers.SensorListSerializer
            if self.action == "list"
            else serializers.SensorDetailSerializer
        )


class MeasurementViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = models.Measurement.objects.all()
    serializer_class = serializers.MeasurementSerializer

    back = "hw5"
