from django.db import models


# Create your models here.
class HashTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    descriptor = models.TextField()
    HashTag = models.ManyToManyField(HashTag, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=5, null=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='reviews')
