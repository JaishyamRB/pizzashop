from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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
        #handles auntentication and redirection
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
        return render(request,'pizzashopapp/adminhomepage.html')
