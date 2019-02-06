from django.db import models
from django.core.exceptions import ValidationError


def is_positive(value: int) -> None:
    if value <= 0:
        raise ValidationError('value must be positive')


class Currency(models.Model):
    class Meta:
        verbose_name_plural = 'Currencies'
    code = models.CharField(max_length=3, unique=True)
    exchange = models.FloatField()

    def __str__(self):
        return self.code


class Product(models.Model):
    image = models.ImageField(null=True)
    title = models.CharField(max_length=255)
    price = models.IntegerField(validators=(is_positive,))
    currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL)
    description = models.TextField()

    def __str__(self):
        return '%s (%d)' % (self.title, self.id)


class Order(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.IntegerField(validators=(is_positive,))
    flat = models.IntegerField(validators=(is_positive,))
    item = models.CharField(max_length=255)

