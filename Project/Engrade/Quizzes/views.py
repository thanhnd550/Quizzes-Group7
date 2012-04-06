# Create your views here.
from Engrade.Quizzes.models import Quiz
from django.shortcuts import HttpResponseRedirect,HttpResponse,render_to_response
from django.core.urlresolvers import reverse

def Add_Quiz(request):
    if request.user.is_authenticated() and request.user.is_active:
        title=request.POST.get('title','')
        ques=request.POST.get('question','')
        ans1=request.POST.get('ans1','')
        ans2=request.POST.get('ans2','')
        ans3=request.POST.get('ans3','')
        ans4=request.POST.get('ans4','')
        correct_ans=request.POST.get('correct_ans','')
        created=request.POST.get('create')


        if title or ques or ans1 or ans2 or ans3 or ans4 or correct_ans:
            p=Quiz(
                title=title,
                ques=ques,
                ans1=ans1,
                ans2=ans2,
                ans3=ans3,
                ans4=ans4,
                correct_ans=correct_ans
            )
            p.save()
        all=Quiz.objects.all()

        return render_to_response('Quizzes.html',{
            'title':title,
            'ques':ques,
            'ans1':ans1,
            'ans2':ans2,
            'ans3':ans3,
            'ans4':ans4,
            'correct_ans':correct_ans,
            'created':created,
            'all':all
        })

def DELETE(request,id=''):
    if request.user.is_authenticated() and request.user.is_active:
        Quiz.objects.get(id=id).delete()
        return HttpResponseRedirect(reverse("Engrade.Quizzes.views.Add_Quiz"))

def EDIT(request,id=''):
    if request.user.is_authenticated() and request.user.is_active:
        p=Quiz.objects.get(id=id)

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
            return HttpResponseRedirect(reverse("Engrade.Quizzes.views.Add_Quiz"))
        return render_to_response('Change.html',{
            'new_title':new_title,
            'new_ques':new_ques,
            'new_ans1':new_ans1,
            'new_ans2':new_ans2,
            'new_ans3':new_ans3,
            'new_ans4':new_ans4,
            'new_correct_ans':new_correct_ans,
            'edited':edited
        })

def DISPLAY(request,id=''):
    p=Quiz.objects.get(id=id)
    ok=request.POST.get('ok')
    show=request.POST.get('show_correct_ans')
    if ok:
        return HttpResponseRedirect(reverse("Engrade.Quizzes.views.Add_Quiz"))
    else:
        return render_to_response('show.html',{
            'title':p.title,
            'ques':p.ques,
            'ans1':p.ans1,
            'ans2':p.ans2,
            'ans3':p.ans3,
            'ans4':p.ans4,
            'correct_ans':p.correct_ans,
            'show_correct_ans':show
        })