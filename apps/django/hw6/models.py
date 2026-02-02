from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        default_related_name = "%(model_name)ss"


class Warehouse(BaseModel):
    address = models.CharField(max_length=256, unique=True)
    items = models.ManyToManyField("Item", through="WarehouseItem")

    def __str__(self):
        return self.address

    class Meta(BaseModel.Meta):
        ordering = ["address"]


class Item(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        ordering = ["name"]


class WarehouseItem(BaseModel):
    warehouse = models.ForeignKey("Warehouse", models.CASCADE)
    item = models.ForeignKey("Item", models.CASCADE)
    unit_cost = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    @property
    def total_cost(self) -> int:
        return self.unit_cost * self.quantity

    def __str__(self):
        return f"{self.warehouse} | {self.item}"

    class Meta(BaseModel.Meta):
        ordering = ["warehouse", "item"]
        unique_together = ["warehouse", "item"]
