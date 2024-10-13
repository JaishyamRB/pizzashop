from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages

# Create your views here.
def adminLoginPage(request):
    return render(request,"admin/adminlogin.html")

def adminAuthenticate(request):
   username= request.GET['username']
   password = request.GET['password']

   user = authenticate(username = username, password = password)
   if not user:
       messages.add_message(request,messages.ERROR,"Invalid Credentials")
       return redirect('adminLoginPage')
   else:
       return redirect('adminHomepage')

def adminHomePage(request):
    return render(request,'admin/adminhomepage.html')