from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.cache import add_never_cache_headers
from django.contrib import messages

class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response


@login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')


def SignUpPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm Password are not the same")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render(request,'signup.html')


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login_count=request.session.get('login_count',0)
            print(request.COOKIES)
            login_count=int(login_count)
            login_count=login_count+1
            request.session['login_count']=login_count
            print(f"After incrementing: {request.session.items()}")
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Invalid password/username")
            return render(request, 'login.html')


    return render(request,'login.html')
def LogoutPage(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def HomePage(request):
    username = request.user.username if request.user.is_authenticated else None
    login_count = request.session.get('login_count', 0)
    return render(request, 'home.html', {'username':username,'login_count':login_count})
