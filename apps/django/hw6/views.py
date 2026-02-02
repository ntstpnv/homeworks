from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from apps.common import views
from . import serializers, models


class MenuView(views.MenuView):
    template_name = "hw6/goods.html"

    title = "Склады и товары"
    back = "django"

    def get_queryset(self):
        return {
            "warehouses": settings.LINK("Warehouse List", "warehouse-list"),
            "warehouse_detail": [
                settings.LINK(warehouse.address, "warehouse-detail", warehouse.id)
                for warehouse in models.Warehouse.objects.all()
            ],
            "items": settings.LINK("Item List", "item-list"),
            "item_detail": [
                settings.LINK(item.name, "item-detail", item.id)
                for item in models.Item.objects.all()
            ],
        }


class BasePageNumberPagination(PageNumberPagination):
    page_size = 2


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = models.Warehouse.objects.all()
    serializer_class = serializers.WarehouseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["items"]
    search_fields = ["address", "items__name", "items__description"]
    pagination_class = BasePageNumberPagination


class ItemViewSet(viewsets.ModelViewSet):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "description"]
    pagination_class = BasePageNumberPagination
