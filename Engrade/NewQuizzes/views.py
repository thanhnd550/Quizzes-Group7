# Create your views here.
from NewQuizzes.models import Question,Title,Assign_To
from django.shortcuts import HttpResponseRedirect,render_to_response
from django.core.urlresolvers import reverse
from classes.models import Class
import datetime
from django.db.models import Q

def Create_Quiz(request):
    if request.user.is_authenticated() and request.user.is_active:
        title=request.POST.get('title','')
        Created=request.POST.get('create')
        TimeLimit=request.POST.get('TimeLimit')

        if title:
            p=Title(title=title,update_time=datetime.datetime.now(),Time_limit=int(TimeLimit),user_quiz=request.user.username)
            p.save()
        list=Title.objects.filter(user_quiz=request.user.username)
        return render_to_response('Create_Quiz.html',{
            'title':title,
            'list':list,
            'create':Created,
            'user':request.user
        })
    else:
        return HttpResponseRedirect(reverse("Engrade.Account.views.Home_page"))

def Add_Question(request,id=''):

    if request.user.is_authenticated() and request.user.is_active:
        p=Title.objects.get(id=id)
        ques=request.POST.get('question','')
        ans1=request.POST.get('ans1','')
        ans2=request.POST.get('ans2','')
        ans3=request.POST.get('ans3','')
        ans4=request.POST.get('ans4','')
        correct_ans=request.POST.get('correct_ans','')
        created=request.POST.get('create')


        if ques or ans1 or ans2 or ans3 or ans3 or ans4 or correct_ans:
            p=Question(
                title=p.title,
                ques=ques,
                ans1=ans1,
                ans2=ans2,
                ans3=ans3,
                ans4=ans4,
                correct_ans=correct_ans,
                number=id
            )
            p.save()
        list=Question.objects.filter(number=id)

        return render_to_response('Add_Question.html',{
                'ques':ques,
                'ans1':ans1,
                'ans2':ans2,
                'ans3':ans3,
                'ans4':ans4,
                'correct_ans':correct_ans,
                'list':list,
                'created':created,
                'user':request.user,
                'mytitle': p.title,
                'number': p.id,
         })
    else:
        return HttpResponseRedirect(reverse("Engrade.Account.views.Home_page"))

def Delete_Title(request,id=''):
    p=Title.objects.get(id=id)
    list=Question.objects.filter(number=p.id)
    list1=Assign_To.objects.filter(number=p.id)
    for e in list:
        e.delete()
    for a in list1:
        a.delete()
    p.delete()
    return HttpResponseRedirect(reverse("Engrade.NewQuizzes.views.Create_Quiz"))
def Edit_Title(request,id=''):

    if request.user.is_authenticated() and request.user.is_active:
        p=Title.objects.get(id=id)
        new_title=request.POST.get('newTitle',p.title)
        TimeLimit=request.POST.get('TimeLimit')
        edited=request.POST.get('edit')
        cancel=request.POST.get('cancel')

        if new_title:
            p.title=new_title
        if TimeLimit:
            p.Time_limit=TimeLimit
        p.save()
        if edited or cancel:
            return HttpResponseRedirect(reverse("Engrade.NewQuizzes.views.Create_Quiz"))
        else:
            return render_to_response('Edit_Title.html',{'newTitle':new_title,
                                                    'edited':edited,
                                                    'obj':p,
            })
    else:
        return HttpResponseRedirect(reverse("Engrade.Account.views.Home_page"))
def Delete_Question(request,id=''):
    p=Question.objects.get(id=id)
    q=Title.objects.get(id=p.number)
    p.delete()
    return HttpResponseRedirect(reverse("Engrade.NewQuizzes.views.Add_Question",args=str(q.id)))
def Edit_Question(request,id=''):

    if request.user.is_authenticated() and request.user.is_active:
        p=Question.objects.get(id=id)
        q=Title.objects.get(id=p.number)

        edited=request.POST.get('edit')
        new_title=request.POST.get('new_title',p.title)
        new_ques=request.POST.get('new_question',p.ques)
        new_ans1=request.POST.get('new_ans1',p.ans1)
        new_ans2=request.POST.get('new_ans2',p.ans2)
        new_ans3=request.POST.get('new_ans3',p.ans3)
        new_ans4=request.POST.get('new_ans4',p.ans4)
        new_correct_ans=request.POST.get('new_correct_ans','')

        if new_title or new_ques or new_ans1 or new_ans2 or new_ans3 or new_ans4 or new_correct_ans:
            if new_title:
                p.title=new_title
            if new_ques:
                p.ques=new_ques
            if new_ans1:
                p.ans1=new_ans1
            if new_ans2:
                p.ans2=new_ans2
            if new_ans3:
                p.ans3=new_ans3
            if new_ans4:
                p.ans4=new_ans4
            if new_correct_ans:
                p.correct_ans=new_correct_ans

            p.save()
        if edited:
            return HttpResponseRedirect(reverse("Engrade.NewQuizzes.views.Add_Question",args=str(q.id)))
        return render_to_response('Edit_Question.html',{
            'new_ques':new_ques,
            'new_ans1':new_ans1,
            'new_ans2':new_ans2,
            'new_ans3':new_ans3,
            'new_ans4':new_ans4,
            'new_correct_ans':new_correct_ans,
            'edited':edited,
            'correct':p.correct_ans,
            'number':p.id,
        })
    else:
        return HttpResponseRedirect(reverse("Engrade.Account.views.Home_page"))

def Assign_to(request,id=''):
    class_list=request.POST.getlist('class')
    submit=request.POST.get('submit')

    qset=(
        Q(number__icontains=id)
    )
    assigned=Assign_To.objects.filter(qset).distinct()
    number_list=[]
    for e in assigned:
        number_list.append(str(e.number_class))
    for cl in class_list:
        if cl not in number_list:
            p=Assign_To(number_class=cl,number=id)
            p.save()
    list=Class.objects.filter(teacher=request.user.username)
    AssignedList=[]
    for cls in list:
        for ass in number_list:
            if str(cls.id) == ass:
                AssignedList.append(cls)

    if submit:
        return HttpResponseRedirect(reverse("Engrade.NewQuizzes.views.Create_Quiz"))
    return render_to_response('assign_to.html',{
        'list':list,
        'assigned':AssignedList,
    })

