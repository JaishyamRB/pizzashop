from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product

context = {"Products":Product.objects.all()}

# Create your views here.

def adminLogout(request):
    logout(request)
    return redirect('pizzashopapp:adminLoginPage')

# rewriting views as class

class AdminLoginPage(generic.TemplateView):
    def get(self,request,*args,**kwargs):
        #handles login page and redirection 
        if request.user.is_authenticated:
            return redirect('pizzashopapp:adminHomepage')
        return render(request,'pizzashopapp/adminlogin.html')
    
    def post(self,request,*args,**kwargs):
       
       action = request.POST.get('action',None)
       #handles auntentication and redirection
       if not action:
           username= request.POST['username']
           password = request.POST['password']

           user = authenticate(username = username, password = password)
           if user:
            login(request,user)
            return redirect('pizzashopapp:adminHomepage')
           else:
            messages.add_message(request,messages.ERROR,"Invalid Credentials")
            return redirect('pizzashopapp:adminLoginPage')

class AdminHomePage(LoginRequiredMixin,generic.TemplateView):
    login_url = "/admin/"
    
    def get(self,request,*args,**kwargs):
        #handles redirecion based on authentication
        return render(request,'pizzashopapp/adminhomepage.html',context)
    
    def post(self,request,*args,**kwargs):
       action = request.POST.get('action_name')
       if action == "add_product":
          print(request.POST['name'],request.POST['price'])
          product = Product(name = request.POST['name'], price = request.POST['price'])
          product.save()
          print("+++++",product,"+++++")
        #   self.get(self,request,*args,**kwargs)
       
       elif action == "delete_product":
        Product.objects.filter(id = request.POST.get('product_pk')).delete()

       elif action == "edit_product":
          current_product = Product.objects.filter(id = request.POST.get('product_pk'))[0]
          current_product.name = request.POST.get('name')
          current_product.price = request.POST.get('price')
          current_product.save()

       context = {"Products":Product.objects.all()}
       return render(request,'pizzashopapp/adminhomepage.html',context)
        
        
