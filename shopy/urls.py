"""shopy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home,)
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),                            
    path("", views.home),
    path("editProduct/<int:id>", views.editprod),
    path("contact/", views.contact),
    path("subscribe/", views.subs,),
    path("about/", views.about,),
    path("success/<str:rppid>/<str:rpoid>/<str:rpsid>", views.success,),
    path("enterOTP/<str:username>", views.enterOTP,),
    path("enterpass/<str:username>", views.enterPass,),
    path("resetPass/", views.resetPass),
    path("login/", views.login),
    path("logout/", views.logout),
    path("update/", views.update),
    path("addcart/<int:num>", views.addcart),
    path("cart/", views.viewcart),
    path("addprod/", views.addprod),
    path("profile/", views.profile),
    path("buynow/<int:id>", views.buynow),
    path("checkout/", views.checkout,),
    path("cancelorder/<int:id>", views.cancelorder,),
    path("updateQ/<int:id>", views.updateQuan,),
    path("shop/<str:mc>/<str:brn>/", views.shop),
    path("product/<int:id>/", views.productPage),
    path("delproduct/<int:id>/", views.delprod),
    path("delwish/<int:id>/", views.delwish),
    path("delimg/<int:id>/<int:prid>/", views.delimg),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


