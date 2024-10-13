from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def adminLoginPage(request):
    if request.user.is_authenticated:
        return render(request,'admin/adminhomepage.html')
    return render(request,"admin/adminlogin.html")

def adminAuthenticate(request):
   username= request.GET['username']
   password = request.GET['password']

   user = authenticate(username = username, password = password)
   if not user:
       messages.add_message(request,messages.ERROR,"Invalid Credentials")
       return redirect('adminLoginPage')
   else:
       login(request,user)
       return redirect('adminHomepage')
   
@login_required(login_url="/admin/")
def adminHomePage(request):
    return render(request,'admin/adminhomepage.html')

def adminLogout(request):
    logout(request)
    return redirect('adminLoginPage')
