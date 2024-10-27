from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    
    @property
    def total_price(self):
        total = 0
        for line in self.cartline_set.filter(cart=self.id):
            if line.product:  # Check if product is not None
                total += line.product.price * line.quantity
        return total

class CartLine(models.Model):
    quantity = models.IntegerField() 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

class Customer(models.Model):
    def __str__(self):
        return self.user.username

    email = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart,on_delete=models.SET_NULL, null=True)

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)

    @property
    def total_price(self):
        total = 0
        for line in self.orderline_set.filter(order=self.id):
            if line.product:  # Check if product is not None
                total += line.product.price * line.quantity
        return total
    
class OrderLine(models.Model):
    quantity = models.IntegerField() 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
