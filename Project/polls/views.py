# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Template, Context
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login


def login(request):
    username=request.POST.get('username')
    password = request.POST.get('password')
    remember=request.POST.get('remember me')

    user=auth.authenticate(name=username,password=password)
    if user is not None and  user.is_active:
        login(request,user)
        return HttpResponseRedirect('MainPage')
    else:
        return HttpResponseRedirect('home_page')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("login")


def main_page(request):
    if request.user.is_authenticated() and request.user.is_active:
        return render_to_response('Main-page.html',{'user': request.user})
    else:
        return HttpResponseRedirect('login')


def Home_page(request):
    return render_to_response('Home-page.html')