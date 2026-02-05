from rest_framework import serializers

from . import models


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Warehouse
        fields = ["address", "items"]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = "__all__"


# class WarehouseItemSerializer(serializers.ModelSerializer):
#     item_id = serializers.PrimaryKeyRelatedField(
#         queryset=models.Item.objects.all(), source="item", write_only=True
#     )
#     item = ItemSerializer(read_only=True)
#
#     class Meta:
#         model = models.WarehouseItem
#         fields = ["item_id", "item", "unit_cost", "quantity", "total_cost"]
