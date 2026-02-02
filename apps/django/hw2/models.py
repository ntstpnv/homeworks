from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True, max_length=64)
    image = models.ImageField()

    ingredients = models.ManyToManyField("Ingredient", "dishes", through="Recipe")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Ingredient(models.Model):
    name = models.CharField(max_length=64, unique=True)

    unit = models.ForeignKey("Unit", models.PROTECT, "ingredients")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Unit(models.Model):
    name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Recipe(models.Model):
    dish = models.ForeignKey("Dish", models.CASCADE)
    ingredient = models.ForeignKey("Ingredient", models.CASCADE)

    amount = models.PositiveSmallIntegerField()

    class Meta:
        default_related_name = "recipe"
        unique_together = ["dish", "ingredient"]
