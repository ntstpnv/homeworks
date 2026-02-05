from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Measurement(models.Model):
    sensor = models.ForeignKey("Sensor", models.CASCADE, "measurements")

    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at.strftime('%H:%M:%S %d.%m.%y')} | {self.sensor}"

    class Meta:
        ordering = ["-created_at"]
