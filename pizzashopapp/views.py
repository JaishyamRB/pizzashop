from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic

# Create your views here.

# def adminLoginPage(request):
#     if request.user.is_authenticated:
#         # return render(request,'pizzashopapp/adminhomepage.html')
#         return "pizzashopapp/adminhomepage.html"
#     # return render(request,"pizzashopapp/adminlogin.html")
#     return "pizzashopapp/adminlogin.html"

# def adminAuthenticate(request):
#    username= request.GET['username']
#    password = request.GET['password']

#    user = authenticate(username = username, password = password)
#    if not user:
#        messages.add_message(request,messages.ERROR,"Invalid Credentials")
#        return redirect('adminLoginPage')
#    else:
#        login(request,user)
#        return redirect('pizzashopapp:adminHomepage')
   
@login_required(login_url="/admin/")
def adminHomePage(request):
    return render(request,'pizzashopapp/adminhomepage.html')

def adminLogout(request):
    logout(request)
    return redirect('pizzashopapp:adminLoginPage')

# rewriting the as class based views
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


