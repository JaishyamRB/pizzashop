from django.db import models

# Create your models here.
class Product(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Customer(models.Model):
    email = models.CharField(max_length=50)
    userid = models.IntegerField()