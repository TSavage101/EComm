from django.db import models
from datetime import datetime

TYPE = (
    ('food','FOOD'),
    ('snacks', 'SNACKS'),
    ('clothes','CLOTHES'),
    ('shoes','SHOES'),
    ('accessories','ACCESSORIES'),
    ('gadgets','GADGETS'),
    ('miscellaneous','MISCELLANEOUS'),
)

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    commission = models.DecimalField(decimal_places=2, max_digits=100, default=0)
    picture1 = models.ImageField(upload_to='pics', default='cart.png')
    picture2 = models.ImageField(upload_to='pics', default='cart.png', blank=True, null=True)
    picture3 = models.ImageField(upload_to='pics', default='cart.png', blank=True, null=True)
    picture4 = models.ImageField(upload_to='pics', default='cart.png', blank=True, null=True)
    picture5 = models.ImageField(upload_to='pics', default='cart.png', blank=True, null=True)
    seller = models.CharField(max_length=150)
    seller_email = models.EmailField(max_length=100)
    seller_telegram_number = models.CharField(max_length=12)
    seller_whatsapp_number = models.CharField(max_length=12)
    seller_instagram_number = models.CharField(max_length=12, default="@instagram")
    type = models.CharField(max_length=20, choices=TYPE, default="miscellaneous")
    sales = models.IntegerField(default=0)
    details = models.TextField(default="No details on this product")
    rating = models.IntegerField(default=3)
    arating = models.DecimalField(default=3, max_digits=2, decimal_places=1)
    amount = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=datetime.now)
    featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} sold by {self.seller} "
    
class Rating(models.Model):
    user = models.CharField(max_length=200)
    rating = models.IntegerField(default=3)
    product = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.product} - {self.rating} stars"

class Number(models.Model):
    user = models.CharField(max_length=200)
    number = models.IntegerField(default=1)
    product = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.user} bought {self.number} {self.product}"
    
class Feedback(models.Model):
    user = models.CharField(max_length=200)
    feedback = models.TextField(default="No feedback")
    rating = models.IntegerField(default=3)
    product = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.user} feedback on {self.product}"

class Cart(models.Model):
    user = models.CharField(max_length=200)
    number = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user}'s cart with {self.number} items"
    
class Cart_item(models.Model):
    user = models.CharField(max_length=200)
    product = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.product} is in {self.user}'s cart"
    