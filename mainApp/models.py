from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class mainCategory(models.Model):
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name 

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    maincat=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    props=models.TextField()
    banPic=models.ImageField(upload_to='productimg/')
    baseprice=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)
    finalPrice=models.IntegerField(default=0)
    color=models.CharField(max_length=20)
    size=models.CharField(max_length=10)
    desc=models.TextField()
    stock=models.BooleanField(default=True)
    time=models.DateField(auto_now=True)
    
    def __str__(self):
        return str(self.id)+ " "+ self.name
    
class Pics(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='productimg/')

    def __str__(self):
        return str(self.id)
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    prodId=models.ForeignKey(Product,on_delete=models.CASCADE)

    q=models.IntegerField(default=1)
    def __str__(self):
        return str(self.prodId)

class Profile(models.Model):
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=70)
    username=models.CharField(max_length=50, unique=True)
    phone=models.IntegerField()
    actype=models.CharField(max_length=50)
    pin=models.IntegerField(blank=True,null=True)
    city=models.CharField(max_length=50, default="",null=True,blank=True)
    state=models.CharField(max_length=50, default="",null=True,blank=True)
    otp=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.id) + " " + self.name


ORDER_STATUS = ((1, 'Not Packed'),(2, 'Ready for Shipment'),(3, 'Shipped'),(4,'Delivered'))
PAYMENT_STATUS = ((1, 'Pending'),(2, 'Success'))
PAYMENT_CHOICES = ((1, 'COD'),(2, 'Credit Card'),(3, 'Net Banking'))


class Checkout(models.Model):
    id=models.AutoField(primary_key=True)
    buyer=models.ForeignKey(Profile,on_delete=models.CASCADE)
    products=models.TextField()
    total=models.IntegerField()
    shipping=models.IntegerField()
    finalAmt=models.IntegerField()
    time=models.DateField(auto_now=True)
    active=models.BooleanField(default=True)
    mode=models.IntegerField(choices=PAYMENT_CHOICES,default=1) 
    orderStatus=models.IntegerField(choices=ORDER_STATUS,default=1)
    paymentStatus=models.IntegerField(choices=PAYMENT_STATUS,default=1)
    orderid=models.CharField(max_length=500,null=True,blank=True)
    razor_payment_id=models.CharField(max_length=500,null=True,blank=True)
    razor_sign=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.active)+" "+str(self.buyer)

class Subscribers(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.EmailField(max_length=60)

    def __str__(self):
        return self.email
    
class ContactUS(models.Model):
    name=models.TextField()
    email=models.EmailField(max_length=60)
    subject=models.TextField()
    message=models.TextField()
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.subject+' '+str(self.active)
