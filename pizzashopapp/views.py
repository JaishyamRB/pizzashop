from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product,Customer,Cart,CartLine,Product,Order,OrderLine

context = {"Products":Product.objects.all()}

# Create your views here.
def userLogout(request):
    su = request.user.is_superuser 
    logout(request)
    if su:
       return redirect('pizzashopapp:adminLoginPage')
    return redirect('pizzashopapp:customerHomePage')

def userLogin(request):
   username= request.POST['username']
   password = request.POST['password']
   user = authenticate(username = username, password = password)

   if user:
    login(request,user)
    #   #redirect to admin page
    if user.is_superuser:
        return redirect('pizzashopapp:adminHomepage')
    else:
       #redirect to customer home page
       return redirect('pizzashopapp:customerHomePage')
   else:
      #add error message and redirect to login/signp page
      messages.add_message(request,messages.ERROR,"Invalid Credentials")
      return redirect('pizzashopapp:customerLoginPage')
# rewriting views as class

class AdminLoginPage(generic.TemplateView):
    def get(self,request,*args,**kwargs):
        #handles login page and redirection 
        if request.user.is_authenticated:
            return redirect('pizzashopapp:adminHomepage')
        return render(request,'pizzashopapp/adminlogin.html',context)
    
    def post(self,request,*args,**kwargs):
       
       action = request.POST.get('action',None)
       #handles auntentication and redirection
       if not action:
          return userLogin(request)

class AdminHomePage(LoginRequiredMixin,generic.TemplateView):
    login_url = "/admin/"
    
    def get(self,request,*args,**kwargs):
        #handles redirecion based on authentication
        context = {"Products":Product.objects.all(),
                   "current_orders":Order.objects.filter(completed=False),
                   "completed_orders":Order.objects.filter(completed=True)}
        if request.user.is_superuser:
           return render(request,'pizzashopapp/adminhomepage.html',context)
        return redirect('pizzashopapp:customerHomePage')
    
    def post(self,request,*args,**kwargs):
       action = request.POST.get('action_name')
       if action == "add_product":
          product = Product(name = request.POST['name'], price = request.POST['price'])
          product.save()
       
       if action == "delete_product":
        Product.objects.filter(id = request.POST.get('product_pk')).delete()

       if action == "edit_product":
          current_product = Product.objects.filter(id = request.POST.get('product_pk'))[0]
          current_product.name = request.POST.get('name')
          current_product.price = request.POST.get('price')
          current_product.save()

       if action == "order_complete":
          order = Order.objects.get(id=int(request.POST.get('order_pk')))
          order.completed = True
          order.save()

       return redirect("pizzashopapp:adminHomepage")
        
class CustomerHomePage(generic.TemplateView):
   def get(self,request,*args,**kwargs):
      context = {"Products":Product.objects.all()}
      return render(request,'pizzashopapp/customerhomepage.html',context)    
   
   def post(self,request,*args,**kwargs):
      action = request.POST.get('action_name')

      if action == "add_to_cart":
         productpk = request.POST['product_id']
         quantity = request.POST['quantity']
         user=request.user

         if user.is_anonymous:
            messages.add_message(request,messages.ERROR,"Please login to add products in cart")
            return redirect("pizzashopapp:customerLoginPage")

         product=Product.objects.get(id=productpk)
         customer = Customer.objects.filter(user=user)[0]
         try:
            cart = Cart.objects.get(user=user)
         except Cart.DoesNotExist:
            cart = Cart(user=user)
            cart.save()

         #if the product is in cart then, update quantity in existing cart line
         try:
            existing_product_cl = CartLine.objects.get(cart=cart,product=product)
            existing_product_cl.quantity += int(quantity)
            existing_product_cl.save()
         
         #else create new cartline
         except CartLine.DoesNotExist:
            cart.cartline_set.create(product=product,quantity=quantity)
            customer.cart = cart
            customer.save()

      return redirect('pizzashopapp:customerHomePage')

class CustomerLoginPage(generic.TemplateView):
   def get(self,request,*args,**kwargs):
      return render(request,'pizzashopapp/customerlogin.html')
   
   def post(self,request,*args,**kwargs):
      action = request.POST.get("action_name")

      if action == "singup_user":
         name = request.POST.get("username")
         email = request.POST.get("email")
         password = request.POST.get("password")
         password1 = request.POST.get("password1")

         #if user exisit in DB redirect to singup page with error
         if User.objects.filter(username=name).exists():
            messages.add_message(request,messages.ERROR,"This user already exisits try logging in")
            return redirect('pizzashopapp:customerLoginPage')
         #if passwords dont match rediredct to signup page
         elif password != password1:
            messages.add_message(request,messages.ERROR,"The passwords should match")
            return redirect('pizzashopapp:customerLoginPage')
         #if everything correct signup user and redirect to homepage
         else:
            new_user = User.objects.create_user(username=name,password=password1)
            Customer(email=email,user=new_user).save()
            return userLogin(request)
     
      if action == "login_user":
         return userLogin(request)
    
class MyCart(generic.TemplateView):
   def get(self,request,*args,**kwargs):
      user = request.user

      if user.is_anonymous :
         context = {"Products":Product.objects.all()}
         return redirect('pizzashopapp:customerHomePage')   

      try:
         cart = Cart.objects.get(user=user)
         context = {"Products":Product.objects.all(),
              "cart_items":CartLine.objects.filter(cart=cart),
              "total_price":cart.total_price,
              "cart":cart}
         return render(request,"pizzashopapp/cart.html",context)
      except Cart.DoesNotExist:
         messages.add_message(request,messages.ERROR,"The cart is empty")
         return redirect("pizzashopapp:customerHomePage")
   
   def post(self,request,*args,**kwargs):
       action = request.POST.get("action_name")

       if action == "delete_from_cart":
          CartLine.objects.filter(id = request.POST.get("cartline_pk")).delete()
      
       if action == "update_quantity":
          new_quantity = request.POST.get("quantity")
          cart_line = CartLine.objects.get(id = request.POST.get("cartline_pk"))
          cart_line.quantity = new_quantity
          cart_line.save()
         
       if action == "place_order":
          cart = Cart.objects.get(id=int(request.POST['cart_pk']))
          user=request.user
          customer = Customer.objects.filter(user=user)[0]
          order = Order(user=customer)
          order.save()
          
          for line in cart.cartline_set.all():
             order.orderline_set.create(quantity=line.quantity,product=line.product)
          
          order.save()

          #delete cart once order is placed
          cart.delete()
          return redirect('pizzashopapp:customerHomePage')
       


       return redirect('pizzashopapp:myCart')




