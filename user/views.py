from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from user.models import Address


# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect("all_books")
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        user_name=request.POST.get('user_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(first_name)
        
        user_exist=False
        if User.objects.filter(username=user_name).exists():
            #print("email is already taken")
            messages.error(request,"User name is already taken try with a new one")
            user_exist=True
        if User.objects.filter(email=email).exists():
           # print("email is already taken")
            messages.error(request,"User name is already taken try with a new one")
            user_exist=True
        if user_exist:
            return render(request,'user/signup.html')
        user= User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=user_name,
            password=password
        )
        user.save()
        messages.success(request,"Account created sucessfully. Login to Continue")
    return render(request,'user/signup.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect("all_books")
    if request.method== "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request,username=username,password=password)
        if user is None:
            messages.error(request,"Invalid Username or password")
            return render(request,'user/signin.html')
        else:
            login(request,user)
            return redirect("all_books")
    return render(request,'user/signin.html')

def signout(request):
    logout(request)
    #return redirect(request,'signin')
    return render(request,'user/signin.html')

@login_required(login_url='/usersignin')
def profile(request):
    return render(request,'user/profile.html')


def add_address(request):
    if request.method=="POST":
        address_line_one=request.POST.get('address_line_one')
        address_line_two=request.POST.get('address_line_two')
        locality=request.POST.get('locality')
        landmark=request.POST.get('landmark')
        city=request.POST.get('city')
        state=request.POST.get('state')
        country=request.POST.get('country')
        zip=request.POST.get('zip')
        mobile=request.POST.get('mobile')
        
        address=Address(
            user=request.user,
            address_line_one=address_line_one,
            address_line_two=address_line_two,
            locality=locality,
            landmark=landmark,
            city=city,
            state=state,
            country=country,
            zip=zip,
            mobile=mobile
            
        )
        print(address)
        address.save()
    return redirect('check_out')
