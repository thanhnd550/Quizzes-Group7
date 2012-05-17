# Create your views here.
from django.contrib.auth.models import User
from NewQuizzes.models import Question,Title,Assign_To,OtherUser
from django.shortcuts import HttpResponseRedirect,render_to_response
from django.core.urlresolvers import reverse
from classes.models import Class
import datetime
from django.db.models import Q

#this function allows user create new quiz
#each user only can manage your quizzes
def Create_Quiz(request):
    if request.user.is_authenticated() and request.user.is_active:
        title=request.POST.get('title','')
        TimeLimit=request.POST.get('TimeLimit')

        ok=False
        if title:
            p=Title(title=title,update_time=datetime.datetime.now(),Time_limit=int(TimeLimit),user_quiz=request.user.username)
            p.save()
            ok=True
        if ok:
            return HttpResponseRedirect("/Create_Quizzes/")
        list=[]
        new_list=[]
        for quiz in Title.objects.filter(user_quiz=request.user.username):
            list.append(quiz)
        list_extra_user=OtherUser.objects.all()#list all of user can use this quiz,these users was allow by user created this quiz
        for new_user in list_extra_user:
            if new_user.extra_user==request.user.username:
                if new_user.change:
                    list.append(Title.objects.get(id=new_user.number))#append more quizzes that this user can use.
                else :
                    new_list.append(Title.objects.get(id=new_user.number))
        new_list_ques=[]
        for i in Question.objects.all():
            if Title.objects.get(id=i.number) in new_list:
                new_list_ques.append(i)

        list_ques=[]
        for i in Question.objects.all():
            if Title.objects.get(id=i.number) in list:
                list_ques.append(i)

        return render_to_response('Create_Quiz.html',{
            'title':title,
            'list':list,
            'list_ques':list_ques,
            'new_list':new_list,
            'new_list_ques': new_list_ques,
            'user':request.user
        })
    else:
        return HttpResponseRedirect("/login/")

def Add_User_Quiz(request,id=''):
    p1=Title.objects.get(id=id)
    listUser=OtherUser.objects.filter(number=id)
    state=0
    for u in listUser:
        if u.extra_user==request.user.username:
            if not u.change:
                state=1
                break
            else:
                state=0
                break
    if request.user.username==p1.user_quiz:
        state=0

    if request.user.is_authenticated() and request.user.is_active and state==0:
        p=Title.objects.get(id=id)
        new_user=request.POST.get('new_user','')
        userList=User.objects.all()
        ok = 0
        for u in userList:
            if u.username==new_user:
                ok = 1
        choice=request.POST.get('choice')
        older_user=OtherUser.objects.filter(number=id)
        checkUser=[]
        if older_user:
            for u in older_user:
                if u.extra_user==new_user:
                    checkUser.append(u)

        state1=""
        if new_user:
            if not checkUser and new_user != request.user.username and ok == 1:
                q=OtherUser(
                    number=id,
                    extra_user=new_user,
                    change=int(choice)
                )
                q.save()
                state1=""
            else:
                if new_user==request.user.username:
                    state1=new_user+" is own quiz. "+"You can not add "+new_user
                if checkUser:
                    state1="This user have been added"
                if not ok:
                    state1="No account names " + new_user

        list=OtherUser.objects.filter(number=id)
        return render_to_response('AddUser.html',{
            'createdUser':p.user_quiz,
            'list':list,
            'state':state1,
            'user':request.user,

        })
    else:
        return HttpResponseRedirect("/troll/")
def Delete_User(request,id=''):
    if request.user.is_authenticated() and request.user.is_active:
        p=OtherUser.objects.get(id=id)
        q=Title.objects.get(id=p.number)
        listUser=OtherUser.objects.filter(number=q.id)
        state=0
        for u in listUser:
            if u.extra_user==request.user.username:
                if not u.change:
                    state=1
                    break
                else:
                    state=0
                    break
        if request.user.username==q.user_quiz:
            state=0
        if state==0:
            p.delete()
        return HttpResponseRedirect("/Add_User/"+str(q.id))
    else:
        return HttpResponseRedirect("/troll/")

def Add_Question(request,id=''):
    t=Title.objects.get(id=id)
    listUser=OtherUser.objects.filter(number=id)
    state=0
    for u in listUser:
        if u.extra_user==request.user.username:
            if not u.change:
                state=1
                break
            else:
                state=0
                break
    if request.user.username==t.user_quiz:
        state=0
    if request.user.is_authenticated() and request.user.is_active and state==0:
        q=Title.objects.get(id=id)
        ques=request.POST.get('question','')
        ans1=request.POST.get('ans1','')
        ans2=request.POST.get('ans2','')
        ans3=request.POST.get('ans3','')
        ans4=request.POST.get('ans4','')
        correct_ans=request.POST.get('correct_ans','')
        created=request.POST.get('create')

        ok=False
        if ques or ans1 or ans2 or ans3 or ans3 or ans4 or correct_ans:
            p=Question(
                title=q.title,
                ques=ques,
                ans1=ans1,
                ans2=ans2,
                ans3=ans3,
                ans4=ans4,
                correct_ans=correct_ans,
                number=id
            )
            p.save()
            ok=True
        list=Question.objects.filter(number=id)
        if ok:
            return HttpResponseRedirect("/Add_Question/"+str(q.id))
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
                'mytitle': q.title,
                'number': q.id,
                'state': state,
         })
    else:
        return HttpResponseRedirect("/login/")

def Delete_Title(request,id=''):
    p=Title.objects.get(id=id)
    listUser=OtherUser.objects.filter(number=id)
    state=0
    for u in listUser:
        if u.extra_user==request.user.username:
            if not u.change:
                state=1
                break
            else:
                state=0
                break
    if request.user.username==p.user_quiz:
        state=0
    if request.user.is_authenticated() and request.user.is_active and state==0:
        p=Title.objects.get(id=id)
        list=Question.objects.filter(number=p.id)
        list1=Assign_To.objects.filter(number=p.id)
        list2=OtherUser.objects.filter(number=p.id)
        for e in list:
            e.delete()
        for a in list1:
            a.delete()
        for u in list2:
            u.delete()
        p.delete()
        return HttpResponseRedirect("/Create_Quizzes/")
    else:
        return HttpResponseRedirect("/")

def Edit_Title(request,id=''):
    p=Title.objects.get(id=id)
    listUser=OtherUser.objects.filter(number=id)
    state=0
    for u in listUser:
        if u.extra_user==request.user.username:
            if not u.change:
                state=1
                break
            if u.change:
                state=0
                break
        else:
            state=1
    if request.user.username==p.user_quiz:
        state=0

    if request.user.is_authenticated() and request.user.is_active and state==0:
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
            return HttpResponseRedirect("/Create_Quizzes/")
        else:
            return render_to_response('Edit_Title.html',{'newTitle':new_title,
                                                    'edited':edited,
                                                    'obj':p,
            })
    else:
        return HttpResponseRedirect("/")
def Delete_Question(request,id=''):
    q=Question.objects.get(id=id)
    t=Title.objects.get(id=q.number)
    listUser=OtherUser.objects.filter(number=id)
    state=0
    for u in listUser:
        if u.extra_user==request.user.username:
            if not u.change:
                state=1
                break
            else:
                state=0
                break
    if request.user.username==t.user_quiz:
        state=0
    if request.user.is_authenticated() and request.user.is_active and state==0:
        p=Question.objects.get(id=id)
        q=Title.objects.get(id=p.number)
        p.delete()
        return HttpResponseRedirect("/Add_Question/"+str(q.id))
    else:
        return HttpResponseRedirect("/")

def Edit_Question(request,id=''):
    q=Question.objects.get(id=id)
    t=Title.objects.get(id=q.number)
    listUser=OtherUser.objects.filter(number=id)
    state=0
    for u in listUser:
        if u.extra_user==request.user.username:
            if not u.change:
                state=1
                break
            else:
                state=0
                break
    if request.user.username==t.user_quiz:
        state=0
    if request.user.is_authenticated() and request.user.is_active and state==0:
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
            return HttpResponseRedirect("/Add_Question/"+str(q.id))
        return render_to_response('Edit_Question.html',{
            'new_ques':new_ques,
            'new_ans1':new_ans1,
            'new_ans2':new_ans2,
            'new_ans3':new_ans3,
            'new_ans4':new_ans4,
            'new_correct_ans':new_correct_ans,
            'edited':edited,
            'correct':p.correct_ans,
            'number':q.id,
        })
    else:
        return HttpResponseRedirect("/")

# class Assign_to allow user assign quiz to student
#the class have been assigned can not assign again
def Assign_to(request,id=''):
    p=Title.objects.get(id=id)
    listUser=OtherUser.objects.filter(number=id)
    state=0
    for u in listUser:
        if u.extra_user==request.user.username:
            if not u.change:
                state=1
                break
            else:
                state=0
                break
    if request.user.username == p.user_quiz:
        state=0
    if request.user.is_authenticated() and request.user.is_active and state==0:
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
    else:
        return HttpResponseRedirect("/")

def Show_Question(request,id=''):
    p=Title.objects.get(id=id)
    if request.user.is_authenticated() and request.user.is_active:
        list_ques=Question.objects.filter(number=id)
        return render_to_response('Show_Question.html',{'list':list_ques,'user':request.user,'title':p.title})
    else:
        return HttpResponseRedirect("/troll/")