from django.db import models
from apps.users.models import User

# Create your models here.


class ProductCategory(models.Model):

    """Моделька категория товаров"""

    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Категории товаров"
        verbose_name = "Категория товаров"


class Product(models.Model):

    """Моделька товаров"""

    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')

    @property
    def category_name(self):
        return self.category.title

    def __str__(self):
        return self.title


class TimerModel(models.Model):

    """Моделька для отслеживанья, времени создания изменения и обновления"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
