# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from Quizz.account.models import RegistrationForm
from Quizz.quiz.models import QuizForm
from django.contrib.auth.models import  User
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
        listQuiz = QuizForm.objects.all()
        return render_to_response('Main-page.html',{'user': request.user, 'listQuiz': listQuiz})
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