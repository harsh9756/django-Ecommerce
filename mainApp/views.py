from django.http import HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth,messages
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from shopy import settings
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from .models import *
import json
# Create your views here.
actype=''
def home(request,):
    global actype
    if ( request.user.is_authenticated and request.user.is_superuser==False ):
            prof=Profile.objects.get(username=request.user)
            actype=prof.actype
            if(actype=='seller'):
               actype=True
            else:
                actype=False
    data=Product.objects.all()
    data=data[::-1]
    return render(request,'index.html',{"data":data,'act':actype})

@login_required(login_url="/login/")
def addcart(request,num):
    if(request.method=="POST"):
        prod=Product.objects.get(id=num)
        buyer=request.user
        wslist=Wishlist.objects.filter(user=buyer)
        flag=False
        for i in wslist:
            if(prod==i.prodId):
                flag=True
                break
        if(flag==False):
            w=Wishlist()
            w.user=buyer
            w.prodId=prod
            w.q=int(request.POST.get("q"))
            w.save()
    return HttpResponseRedirect('/product/{}'.format(num))


def delwish(request,id):
    wish=Wishlist.objects.get(prodId=id)
    wish.delete()
    return HttpResponseRedirect('/cart/')


from django.db.models import Q

def shop(request, mc, brn):
    mainCat = mainCategory.objects.all()
    br = Brand.objects.all()
    pics = Pics.objects.all()
    # Create an empty Q object to build the query dynamically
    filter_query = Q()
    if mc != 'all':
        filter_query &= Q(maincat__name=mc)
    if brn != 'all':
        filter_query &= Q(brand__name=brn)
    data = Product.objects.filter(filter_query)
    return render(request, "shop.html", {"data": data, 'pic': pics, "maincat": mainCat, 'brand': br, 'mc': mc, 'brn': brn, 'act': actype})


def productPage(request,id,):
    data=Product.objects.get(id=id)
    pics=Pics.objects.filter(product=id)
    json_data=json.loads(data.props)
    return render(request,'product.html',{'data':data,'act':actype,'pic':pics,'props':json_data})


def contact(request,):
    if(request.method=='POST'):
        c=ContactUS()
        c.name=request.POST.get('name')
        c.email=request.POST.get('email')
        c.subject=request.POST.get('subject')
        c.message=request.POST.get('message')
        c.save()
        return HttpResponseRedirect('/')
    return render(request,'contact.html',{'act':actype})

def updateQuan(request,id):
    wish=Wishlist.objects.get(prodId=id)
    wish.q=request.POST.get('q')
    wish.save()
    return HttpResponseRedirect('/cart/')


def login(request):
    p=Profile()
    if(request.method == "POST"): 
        typee=request.POST.get('button')
        if (typee=="signup"):
            p.name=request.POST.get('name')
            p.email=request.POST.get('email')
            p.username=request.POST.get('username')
            pword=request.POST.get('password')
            confpword=request.POST.get('confpassword')
            p.phone=request.POST.get('phone')
            p.pin=request.POST.get('pin')
            p.city=request.POST.get('city')
            p.state=request.POST.get('state')
            p.save()
            if(pword==confpword):
                user=User.objects.create_user(username=p.username,password=pword)
                user.set_password(pword)
                user.save()
            elif(confpword!=pword):
                messages.error(request,"Password Mismatch")
        elif(typee=='login'):
            pword=request.POST.get('password')
            p.username=request.POST.get('username')
            user=auth.authenticate(username=p.username,password=pword)
            if user is not None:
                auth.login(request,user)
                if(user.is_superuser):
                    return HttpResponseRedirect('/admin/')
                else:
                    return HttpResponseRedirect('/profile/')
            else:
                messages.error(request,("Invalid Username or Password. Try again..."))
        else:
            pass
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def resetPass(request): 
    if(request.method=="POST"):
        try:
            user=Profile.objects.get(email=request.POST.get('email'))
            import random
            otp=random.randint(1000,9999)
            user.otp=otp
            user.save()
            import smtplib
            from email.message import EmailMessage
            msg=EmailMessage()
            msg['subject'] = 'Password Reset Request'
            msg['from'] = 'WEbsite'
            msg['to'] = user.email
            msg.set_content('Hi {}, Your otp for Password Reset is {}'.format(user.name,otp))
            ser=smtplib.SMTP_SSL("smtp.gmail.com",465)
            ser.login("harshbgmi9756@gmail.com","scmyhpcpyednemgt")
            ser.send_message(msg)
            ser.quit()
            return HttpResponseRedirect('/enterOTP/'+user.username)
        except:
            messages.error(request,"No account associated with Email!")
    return render(request,'forgotpass.html')

def enterOTP(request,username):
    user=Profile.objects.get(username=username)
    if(request.method=='POST'):
        otp=int(request.POST.get('otp'))
        if(otp==user.otp):
            return HttpResponseRedirect('/enterpass/'+user.username)
        else:
            messages.error(request,"Incorrect OTP. Pleas check OTP.")
    return render(request,'enterotp.html')

def enterPass(request,username):
    user=Profile.objects.get(username=username)
    if(request.method=='POST'):
        passw=request.POST.get('password')
        cpassw=request.POST.get('cpassword')
        if(passw==cpassw):
            r=User.objects.get(username=user.username)
            r.set_password(passw)
            r.save()
            return HttpResponseRedirect('/login/')
        else:
            messages.error(request,"Password does not match")
    return render(request,'enterpass.html')


def update(request,):
    seller=Profile.objects.get(username=request.user)
    if(request.method=='POST'):
        seller.name=request.POST.get("name")
        seller.email=request.POST.get("email")
        seller.phone=request.POST.get("phone")
        seller.city=request.POST.get("city")
        seller.state=request.POST.get("state")
        seller.pin=request.POST.get("pin")
        seller.save()
        return HttpResponseRedirect("/profile/")
    return render(request,'update.html',{'data':seller,'act':actype})

def profile(request,):
    buyer=Profile.objects.get(username=request.user)
    prod=Product.objects.filter(user=request.user)
    print(prod)
    checkout=Checkout.objects.filter(buyer=buyer)
    return render(request,"profile.html",{"data":buyer,"checkout":checkout,'prod':prod})


def addprod(request,):
    if(request.method=='POST'):
        p=Product()
        m=mainCategory()
        b=Brand()
        p.name=request.POST.get('name')
        p.user=request.user
        p.maincat=request.POST.get('maincat')
        p.brand=request.POST.get('brand')
        p.banPic=request.FILES.get('banimage')
        stock=request.POST.get('stock')
        if(stock):
            p.stock=True
        else:
            p.stock=False
        p.baseprice=request.POST.get('Bprice')
        p.discount=request.POST.get('discount')
        p.finalPrice=request.POST.get('Fprice')
        p.color=request.POST.get("color")
        p.size=request.POST.get("size")
        p.desc=request.POST.get('desc')
        try:
            foundmc=mainCategory.objects.get(name=p.maincat)
            foundbr=Brand.objects.get(name=p.brand)
        except:
            m.name=p.maincat
            b.name=p.brand
            m.save()
            b.save()
            print(b.name)
        # Properties of product
        counter=request.POST.get('counter')
        counter=int(counter)
        i=0
        propdict = {}
        while(i<counter):
            x=request.POST.get('propkey'+str(i))
            y=request.POST.get('propvalue'+str(i))
            propdict[x]=y
            i+=1
        jsondata=json.dumps(propdict)
        p.props=jsondata
        p.save()
        # Saving multiple images
        images=request.FILES.getlist('addimages')
        for img in images:
            pic=Pics()
            pic.product=p
            pic.img=img
            pic.save()
        return HttpResponseRedirect('/profile/')
    return render(request,'addprod.html',{'act':actype})

def delprod(request,id):
    data=Product.objects.get(id=id)
    data.delete()
    return HttpResponseRedirect("/profile/")


def delimg(request,id,prid):
    data=Pics.objects.get(id=id)
    data.delete()
    return HttpResponseRedirect('/editProduct/{}'.format(prid))


def editprod(request,id):
    data=Product.objects.get(id=id)
    pics=Pics.objects.filter(product=id)
    json_data=json.loads(data.props)
    if(request.method=="POST"):
        data.name=request.POST.get('name')
        data.user=request.user
        data.maincat=request.POST.get('maincat')
        data.brand=request.POST.get('brand')
        data.stock=request.POST.get('stock')
        data.baseprice=request.POST.get('Bprice')
        data.discount=request.POST.get('discount')
        data.finalPrice=request.POST.get('Fprice')
        data.color=request.POST.get("color")
        data.size=request.POST.get("size")
        data.desc=request.POST.get('desc')
        data.props=request.POST.get('jsdata')
        if(request.FILES.get("banPic")!=None):
            data.banPic=request.FILES.get('banimage')
        if(request.FILES.getlist("addimages")!=None):
            images=request.FILES.getlist('addimages')
            for img in images:
                pic=Pics()
                pic.product=data
                pic.img=img
                pic.save()
        data.save()
        return HttpResponseRedirect('/profile/')
    return render(request,"editproduct.html",{"i":data,"act":actype,"pic":pics,"json_data":json_data})

def viewcart(request,):
    products=Wishlist.objects.filter(user=request.user)
    total=0
    shipping=0
    for i in products:
        total=total+i.prodId.finalPrice*i.q
    if total<=1000 and total>0:
        shipping=150
    finalAmt=total+shipping
    return render(request,'cart.html',{'act':actype,"products":products,"total":total,"shipping":shipping,"finalAmt":finalAmt})


def checkout(request):
    buyer=Profile.objects.get(username=request.user)
    cart=Wishlist.objects.filter(user=request.user)
    total=0
    shipping=0
    for i in cart:
        total=total+i.prodId.finalPrice*i.q
    if total<=1000 and total>0:
        shipping=150
    finalAmt=total+shipping
    if(request.method=='POST'):
            c=Checkout()
            c.buyer=buyer
            c.total=0
            c.shipping=0
            c.finalAmt=0
            d={}
            for i in cart:
                d[str(i.prodId.id)]=str(i.q)
                c.total=c.total+i.prodId.finalPrice*i.q
            jsdata=json.dumps(d)
            if(c.total>1000):
                pass
            else:
                c.shipping=150
            c.finalAmt=c.total+c.shipping
            mode=request.POST.get('mode')
            c.products=jsdata
            if(mode=='COD'):
                c.paymentStatus=2
                c.mode=1
                cart.delete()
                c.save()
                messages.success(request,"Your order has been placed successfully")                
                return HttpResponseRedirect('/profile/')
            else:
                c.mode=2
                amount = int(c.finalAmt*100)  # The amount you want to charge in paise (e.g., 1000 for ₹10)
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                payment = client.order.create({"amount": amount, "currency": "INR"})
                c.save()
                return render(request,'pay.html',{'buyer':buyer,'cart':cart,
                                                    'finalAmt':finalAmt,
                                                    'amount':amount,
                                                    'api_key':settings.RAZORPAY_KEY_ID,
                                                    'order_id':payment['id'],
                                                    'user':buyer
                                                    })
    return render(request,"checkout.html",{'buyer':buyer,'cart':cart,'finalAmt':finalAmt})


def buynow(request,id):
    buyer=Profile.objects.get(username=request.user)
    prod=Product.objects.get(id=id)
    c=Checkout()
    c.buyer=buyer
    c.total=prod.finalPrice
    c.shipping=0
    c.products=prod.id
    if c.total<=1000 and c.total>0:
        shipping=150
    c.finalAmt=c.total+shipping
    mode=request.POST.get('mode')
    if(request.method=='POST'):
        if(mode=="COD"):
            c.paymentStatus=2
            c.mode=1
            c.save()
            messages.success(request,"Your order has been placed successfully")                
            return HttpResponseRedirect('/profile/')
        else:
            c.mode=2
            amount = int(c.finalAmt*100)  # The amount you want to charge in paise (e.g., 1000 for ₹10)
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({"amount": amount, "currency": "INR"})
            c.save()
            return render(request,'pay2.html',{'buyer':buyer,'cart':prod,
                                                'finalAmt':c.finalAmt,
                                                'amount':amount,
                                                'api_key':settings.RAZORPAY_KEY_ID,
                                                'order_id':payment['id'],
                                                'user':buyer
                                                })
    return render(request,'buynow.html',{'buyer':buyer,'prod':prod,'final':c.finalAmt})


def success(request,rppid,rpoid,rpsid):
    buyer=Profile.objects.get(username=request.user)
    checkk=Checkout.objects.filter(buyer=buyer)
    cart=Wishlist.objects.filter(user=request.user)
    cart.delete()
    check=checkk[::-1]
    check[0].paymentStatus=2
    check[0].orderid=rpoid
    check[0].razor_payment_id=rppid
    check[0].razor_sign=rpsid
    check[0].save()
    return HttpResponseRedirect('/profile/')
def subs(request):
    if(request.method=='POST'):
        email=request.POST.get('email')
        try:
            e=Subscribers.objects.get(email=email)
        except:
            s=Subscribers()
            s.email=email
            s.save()
        return HttpResponseRedirect('/')
    

def cancelorder(request,id):
    check=Checkout.objects.get(id=id)
    check.delete()
    return HttpResponseRedirect('/profile/')
def about(request):
    return render(request,'about.html')