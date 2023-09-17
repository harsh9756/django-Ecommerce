from django import template
from ..models import *
import json
register =template.Library()

@register.filter("mult")
def  mult(request,i):
    return i.q*i.prodId.finalPrice

@register.filter("orderStatus")
def  orderStatus(request,i):
    if(i.orderStatus==1):
        return  'Not Packed'
    elif(i.orderStatus==2):
        return 'Packed'
    elif(i.orderStatus==3):
        return 'Out for Delivery'
    else:
        return "Delivered"  
@register.filter("payStatus")
def  payStatus(request,i):
    if(i.paymentStatus==1):
        return 'Pending'
    else:
        return 'Completed'
    
@register.filter("payMode")
def  payMode(request,i):
    if(i.paymentStatus==1):
        return 'COD'
    else:
        return 'Online'
    
@register.filter("products")
def  products(request,i):
    prods=i.products
    data=json.loads(prods)
    x=[]
    for key,value in data.items():
        product=Product.objects.get(id=key)
        x.append(product)
    return x

@register.filter("paynow")
def  paynow(request,i):
    if(i.paymentStatus==1):
        return True
    else:
        return False
