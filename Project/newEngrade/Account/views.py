# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from Account.models import RegistrationForm
from django.contrib.auth.models import  User
from django.core.urlresolvers import reverse
def login(request):
    username=request.POST.get('username')
    password = request.POST.get('password')
    remember=request.POST.get('remember me')

    user=auth.authenticate(name=username,password=password)
    if user is not None and  user.is_active:
        login(request,user)
        return HttpResponseRedirect('/Create_Class/')
    else:
        return HttpResponseRedirect(reverse("Account.views.Home_page"))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("Engrade.Account.views.Home_page"))


def main_page(request):
    if request.user.is_authenticated() and request.user.is_active:
        return render_to_response('Main-page.html',{'user': request.user, })
    else:
        return HttpResponseRedirect('login')


def Home_page(request):
    return render_to_response('Home-page.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
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