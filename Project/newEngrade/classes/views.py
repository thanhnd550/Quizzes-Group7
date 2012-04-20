# Create your views here.
from classes.models import Class
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from NewQuizzes.models import Title,Question,Assign_To
from django.core.urlresolvers import reverse
from Account.views import login

def Create_class(request):
    if request.user.is_authenticated() and request.user.is_active:
        name=request.POST.get('name','')
        access_num=request.POST.get('number','')

        if name and access_num:
            p=Class(name=name,access_number=access_num,teacher=request.user.username)
            p.save()
        list=Class.objects.filter(teacher=request.user.username)
        return render_to_response('Create_Class.html',{
            'name':name,
            'number':access_num,
            'list':list,
            'user':request.user,
        })
    else:
        return HttpResponseRedirect("/login/")
def listOfClasses(request):
    listOfClassesCreated=Class.objects.all()
    return render_to_response('ListOfClasses.html',{'list':listOfClassesCreated})

def go_to_class(request,id=''):
    p=Class.objects.get(id=id)

    check="true"
    access=request.POST.get('access','')
    if access:
        if access==p.access_number:
            return HttpResponseRedirect(reverse("Engrade.classes.views.Do_Quizzes",args=str(p.id)))
        if access !=p.access_number:
            check='wrong'
    list=Class.objects.all()
    return render_to_response('go_to_class.html',{
            'access':access,
            'ok':check,
            'list':list,
            'class_name': p.name,
        })

def Do_Quizzes(request,id=''):
    p=Class.objects.get(id=id)
    ass_to=Assign_To.objects.filter(name=p.name)
    queue=[]
    for q in ass_to:
        if Title.objects.get(id=q.number):
            t=Title.objects.get(id=q.number)
            queue.append(t)
    return render_to_response('Do_Quizzes.html',{'list':queue,})

def Do_Question(request,id=''):

    mark=0
    total=0
    list_correct_answer=[]
    lq=Question.objects.filter(number=id)
    submitted=request.POST.get('submit')
    for ques in lq:
        total+=1
        choice_ans=request.POST.get(ques.ques)
        ques.your_answer=choice_ans
        if choice_ans:
            if choice_ans == ques.correct_ans:
                mark=mark+1
                ques.check_do='true'
                list_correct_answer.append(ques)
            else:
                ques.check_do='false'

    return render_to_response('Do_Question.html',{
        'list':lq,
        'mark':mark,
        'submitted':submitted,
        'list_correct':list_correct_answer,
        'total':total,
    })

def show_time(request):
    list=Class.objects.all()
    Next=request.POST.get('next')
    return render_to_response('test.html',{'list':list,'next':Next})