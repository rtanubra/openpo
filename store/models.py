from django.db import models

#link a seller to a user
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email =  models.EmailField(max_length=200,null=True)
    user = models.OneToOneField(User,null=True, on_delete= models.CASCADE)
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email =  models.EmailField(max_length=200,null=True,blank=True)
    seller = models.ForeignKey(Seller, on_delete= models.CASCADE,null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    seller= models.ForeignKey(Seller, on_delete= models.CASCADE,null=True)
    name= models.CharField(max_length=200, null = True)
    description= models.TextField(null=True)
    price = models.FloatField(null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Location(models.Model):
    name= models.CharField(max_length=200, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null =True)
    def __str__(self):
        return self.name

class Basket(models.Model):
    seller = models.ForeignKey(Seller,null=True, on_delete=models.SET_NULL )
    customer = models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL )
    date_created = models.DateField(auto_now_add=True, null=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,null=True)
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    )
    status = models.CharField(max_length=200, null=True,choices= STATUS)
    note= models.TextField(null=True,blank=True)
    pickup_location= models.ForeignKey(Location,on_delete=models.CASCADE, null=True)
    def __str__(self):
        try:
            my_name = self.customer.name + str(self.date_created)
        except:
            my_name = "unknown buyer " +str(self.date_created)
        return my_name
    @property
    def get_basket_total(self):
        orders = self.order_set.all()
        total = sum(order.get_total for order in orders)
        return total 
    
    @property
    def get_basket_items(self):
        orders = self.order_set.all()
        total = sum(order.quantity for order in orders)
        return total
    
    @property
    def get_contents(self):
        contents = "" 
        orders = self.order_set.all()
        for order in orders:
            current_string = " "
            current_string +=  str(order.quantity)
            current_string += ' '
            current_string += order.product.name
            contents += current_string
        return contents
        

class Order(models.Model):
    product = models.ForeignKey(Product,null=True, on_delete=models.CASCADE )
    date_created = models.DateField(auto_now_add=True, null=True)
    basket = models.ForeignKey(Basket, on_delete= models.CASCADE,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    def __str__(self):
        try:
            my_name = self.product.name +":"+ str(self.date_created)
        except:
            my_name =str(self.date_created)
        return my_name
    
    @property
    def get_total(self):
        try:
            total = self.product.price * self.quantity
        except:
            total= 0
        return total 
    
