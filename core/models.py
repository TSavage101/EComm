from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    picture = models.ImageField(upload_to='pics', default='cart.png')
    seller = models.CharField(max_length=150)
    amount = models.IntegerField()