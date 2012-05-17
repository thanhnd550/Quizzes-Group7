# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from Account.models import RegistrationForm
from django.contrib.auth.models import  User
from django.core.urlresolvers import reverse

def mylogin(request):
    username=request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        state=""
        user=auth.authenticate(username=username,password=password)
        if user is not None and  user.is_active:
            login(request,user)
            return HttpResponseRedirect('/Create_Class/')
        else:
            state="Sorry, that's not a valid username or password"
            return render_to_response('registration/login.html',{'state':state})
    else:
        return render_to_response('registration/login.html')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def About(request):
    return render_to_response("About.html")



def Home_page(request):
    return render_to_response('Home-page.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            user.save()
            return HttpResponseRedirect('/success')
    else:
        form = RegistrationForm()
    return render_to_response(
        'registration/register.html',{'form': form}
    )

def success(request):
    return render_to_response('success.html')
def troll(request):
    return render_to_response('troll.html')