"""
URL configuration for pizzashop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import userLogout,AdminLoginPage,AdminHomePage,CustomerHomePage,CustomerLoginPage,MyCart,MyOrder,MyAccount

app_name = "pizzashopapp"

urlpatterns = [
    path('', CustomerHomePage.as_view(), name="customerHomePage"),
    path('login/', CustomerLoginPage.as_view(), name="customerLoginPage"),
    path('mycart/', MyCart.as_view() , name="myCart"),
    path('myorders/', MyOrder.as_view(), name="myOrders"),
    path('myaccount/', MyAccount.as_view(), name="myAccount"),
    path(
        'admin/',
        include([
            path('', AdminLoginPage.as_view(), name= "adminLoginPage"),
            path('home/', AdminHomePage.as_view(), name="adminHomepage"),
            path('logout/',userLogout, name="userLogout")
        ])
    ),
]