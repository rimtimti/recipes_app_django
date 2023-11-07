from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=20, null=False)


class Recipe(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)
    description = models.CharField(verbose_name="Описание", max_length=500)
    steps = models.CharField(verbose_name="Этапы приготовления", max_length=500)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления, мин"
    )
    image = models.ImageField(verbose_name="Фото", upload_to="images/")
    create_at = models.DateTimeField(verbose_name="Создано", auto_now=True)


class Сookbook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
