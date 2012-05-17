# Create your views here.
from classes.models import Class,Can_Access_Class
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from NewQuizzes.models import Title,Question,Assign_To
from django.core.urlresolvers import reverse
from Account.views import login
from django.db.models import Q

def Create_class(request):
    if request.user.is_authenticated() and request.user.is_active:
        name=request.POST.get('name','')
        access_num=request.POST.get('number','')
        choice=request.POST.get('choice')
        show=request.POST.get('show')
        hide=request.POST.get('hide')
        ok=''
        state=""
        state1=""
        qset=(
            Q(access_number__icontains=access_num)
        )
        listAccessNumber=Class.objects.filter(qset).distinct()
        if name and access_num:
            if len(str(access_num))>=6 and(len(str(access_num))<=20) :
                if not listAccessNumber:
                    p=Class(name=name,access_number=access_num,teacher=request.user.username,teacher_email=request.user.email,
                        permission=int(choice)
                    )
                    p.save()
                else:
                    state="This access code have existed.Please enter other code"
            else:
                state="The access code has at least 6 character."
            if len(str(access_num))>20:
                state="the maximum of access code is 20 character."

        list=Class.objects.filter(teacher=request.user.username)
        return render_to_response('Create_Class.html',{
            'name':name,
            'number':access_num,
            'list':list,
            'user':request.user,
            'state':state,
            'show':show,
            'hide':hide,
        })
    else:
        return HttpResponseRedirect("/login/")
def Delete_Class(request,id=''):
    if request.user.is_authenticated() and request.user.is_active:
        p=Class.objects.get(id=id)
        if request.user.username==p.teacher:
            list=Assign_To.objects.filter(number=id)
            for e in list:
                e.delete()
            p.delete()
            return HttpResponseRedirect("/Create_Class/")
        else:
            return HttpResponseRedirect("/login/")
    else:
        return HttpResponseRedirect("/login/")
def listOfClasses(request):
    if request.user.is_authenticated() and request.user.is_active:
        search=request.POST.get('search')
        submit=request.POST.get('submit')
        listOfClassesCreated=Class.objects.all().order_by('teacher')
        listSearch=Class.objects.filter(name=search).order_by('name')
        if not listSearch:
            listSearch=Class.objects.filter(teacher=search).order_by('name')
        new_list=[]
        new_list1=[]
        for cl in listOfClassesCreated:
            my_list=Can_Access_Class.objects.filter(class_number=cl.id)
            for u in my_list:
                if u.user_name==request.user.username:
                  new_list.append(cl)
        for cl in listSearch:
            my_list1=Can_Access_Class.objects.filter(class_number=cl.id)
            for u in my_list1:
                if u.user_name==request.user.username:
                    new_list1.append(cl)
        return render_to_response('ListOfClasses.html',{'list':listOfClassesCreated,'new_list':new_list,'user':request.user,
                                                        'list1':listSearch,'new_list1':new_list1,'submit':submit,
        })
    else:
        return HttpResponseRedirect("/login/")

def go_to_class(request,id=''):
    if request.user.is_authenticated() and request.user.is_active:
        q=Class.objects.get(id=id)
        Allow=Can_Access_Class.objects.filter(class_number=id)
        ok=0
        for u in Allow:
            if request.user.username==u.user_name:
                ok=1
        if q.permission or request.user.username==q.teacher or ok==1:
            p=Class.objects.get(id=id)
            ass_to=Assign_To.objects.filter(number_class=p.id)
            queue=[]
            for a in ass_to:
                if Title.objects.get(id=a.number):
                    t=Title.objects.get(id=a.number)
                    queue.append(t)
            return render_to_response('Do_Quizzes.html',{'list':queue,'class':q.id,'user':request.user})
        else:
            check="true"
            access=request.POST.get('access','')
            if access:
                if access==q.access_number:
                    can_access=Can_Access_Class(class_number=id,can_access=True,user_name=request.user.username)
                    can_access.save()
                    p=Class.objects.get(id=id)
                    ass_to=Assign_To.objects.filter(number_class=p.id)
                    queue=[]
                    for q in ass_to:
                        if Title.objects.get(id=q.number):
                            t=Title.objects.get(id=q.number)
                            queue.append(t)

                    return render_to_response('Do_Quizzes.html',{'list':queue,'class':q.id,'user':request.user})
                if access !=q.access_number:
                    check='wrong'
            list=Class.objects.all()
            return render_to_response('go_to_class.html',{
                    'access':access,
                    'ok':check,
                    'list':list,
                    'class_id': q.id,
                    'user':request.user,
                })
    else:
        return HttpResponseRedirect("/login/")
def Do_Question(request,id='',id1=''):
    p=Class.objects.get(id=id1)
    q=Title.objects.get(id=id)
    listAccessClass=Can_Access_Class.objects.filter(class_number=p.id)
    if request.user.is_authenticated() and request.user.is_active:
        if request.user.username==q.user_quiz or p.permission:
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
                        mark+=1
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

        if not p.permission:
            if listAccessClass:
                for u in listAccessClass:
                    if (request.user.username == u.user_name and u.can_access) or request.user.username==p.teacher:
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
                                    mark+=1
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
                    else:
                        return HttpResponseRedirect("/ListOfClass/")
            else:
                return HttpResponseRedirect("/troll/")

    else:
        return HttpResponseRedirect("/login/")
