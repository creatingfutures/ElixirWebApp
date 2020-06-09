from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import student_status
import json
from django.core import serializers
from user_admin.models import entity,entity_type,entity_status
from user_admin.models import student,facilitator,program,center
from user_admin.models import batch,program_module,module_level,questions,av_question,av_sub_question
from user_admin.models import student_module_level,student_batch,image_question,images_question
import random
import os

def login(request):
    batches=batch.objects.all()
    if request.method=="POST":
        search_query1 = request.POST.get('student', None)
        search_query2 = request.POST.get('batch', None)
        try:
            stud=student.objects.get(pk=int(search_query1))
        except:
            messages.success(request,f'No student of that ID exists')
            return redirect("student_login")
        return redirect('s_home',search_query1,search_query2)
    return render(request,"student_login.html",{"b":batches})



def s_home(request,pk,pk1):
    programs=program.objects.all()
    stud=student.objects.get(student_id=pk)
    return render(request,'s_home.html',{"p1":programs,"pk":pk,"pk1":pk1,"s":stud})


def spoken_english(request,pk,pk1,pk2):
    modules=program_module.objects.filter(program_id=pk2)
    program1=program.objects.get(pk=pk2)
    return render(request,"spoken_english.html",{"m":modules,"pk":pk,"pk1":pk1,"pk2":pk2,"p":program1})

def module_view(request,pk,pk1,pk2,pk3):
    levels=module_level.objects.filter(module_id=pk3).order_by('level_number')
    module=program_module.objects.get(module_id=pk3)
    return render(request,"module_view.html",{"l":levels,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"m":module,"g":'https://www.google.com'})

def crossword(request,pk,pk1,pk2,pk3,pk4):
    module=program_module.objects.get(pk=pk3)
    level=module_level.objects.get(pk=pk4)
    try:
        a="crossword/"+module.module_name+"/"+str(level.level_number)
        b="user_student/templates/crossword/"+module.module_name+"/"+str(level.level_number)
        c=os.getcwd()
        b=c+"/"+b
        length=len([name for name in os.listdir(b)])
        rand=random.randrange(1,length)
        a=a+"/crossword"+str(rand)+".html"
        print(a)
        return render(request,a,{"m":module,"l":level,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3})
    except:
        messages.success(request,f'No Crossword for the level yet')
        return redirect('module_view',pk,pk1,pk2,pk3)


def lesson(request,pk,pk1,pk2,pk3,pk4):
    str1="lesson"
    module = program_module.objects.get(pk=pk3)
    program1=program.objects.get(pk=pk2)
    level=module_level.objects.get(pk=pk4)
    str1=str1+"/"+program1.program_name
    str1=str1+"/"+module.module_name
    str1=str1+"/"+str(level.level_number)
    str1=str1+".html"
    print(str1)
    return render(request,str1)




def before_test(request,pk,pk1,pk2,pk3,pk4):
    module1=program_module.objects.get(pk=pk3)
    level1=module_level.objects.get(pk=pk4)
    return render(request,"before_test.html",
    {"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4,"m":module1,"l":level1})


def standard_test(request,pk,pk1,pk2,pk3,pk4):
    questions1 = sorted(questions.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4).order_by('-pk'),
    key=lambda x: random.random())
    print(questions1,len(questions1))
    data = serializers.serialize('json', questions1)
    print(data)
    request.session['questions'] = data
    module1=program_module.objects.get(pk=pk3)
    level1=module_level.objects.get(pk=pk4)
    i=-1
    return render(request,"standard_test.html",
    {"q":questions1,"score":0,"i":i,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4,"m":module1,"l":level1})

def ajax_standard_test(request,pk,pk1,pk2,pk3,pk4):
    questionss = request.session.get('questions')
    questions1=[]
    for copy in serializers.deserialize("json", questionss):
        questions1.append(copy.object)
    print("QUERUBOI",questions1)
    i = int(request.GET.get('id'))
    c = (request.GET.get('correct'))
    s = int(request.GET.get('score'))
    if c=="True":
        s=s+1
    elif c=="False":
        s=s+0
    i+=1
    if i==len(questions1):
        return render(request,"test_submit.html",
        {"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4,"test_name":"standard","len":len(questions1)})

    if questions1[i].question_type=="Multiple Choice":
        return render(request,"mcq.html",
        {"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})

    if questions1[i].question_type=="Fill Ups":
        return render(request,"fill_ups.html",
        {"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})

    if questions1[i].question_type=="Riddles":
        return render(request,"riddles.html",
        {"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})

    if questions1[i].question_type=="Jumbled Words":
        str=questions1[i].question
        print(str.split())
        return render(request,"jumbled_words.html",
        {"q":questions1,"len":range(0,len(str.split())),"words":str.split(),
        "i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})


def image_test(request,pk,pk1,pk2,pk3,pk4):
    questions1=[]

    images = sorted(images_question.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4).order_by('-pk'),
    key=lambda x: random.random())
    questions1+=images

    image = sorted(image_question.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4).order_by('-pk'),
    key=lambda x: random.random())
    questions1+=image

    print(questions1,len(questions1))
    data = serializers.serialize('json', questions1)
    print(data)
    request.session['questions'] = data
    module1=program_module.objects.get(pk=pk3)
    level1=module_level.objects.get(pk=pk4)
    i=-1
    return render(request,"image_test.html",
    {"q":questions1,"score":0,"i":i,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4,"m":module1,"l":level1})

def ajax_image_test(request,pk,pk1,pk2,pk3,pk4):
    questionss = request.session.get('questions')
    questions1=[]
    for copy in serializers.deserialize("json", questionss):
        questions1.append(copy.object)
    print("QUERUBOI",questions1)
    i = int(request.GET.get('id'))
    c = (request.GET.get('correct'))
    s = int(request.GET.get('score'))
    if c=="True":
        s=s+1
    elif c=="False":
        s=s+0
    i+=1
    if i==len(questions1):
        return render(request,"test_submit.html",
        {"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4,"test_name":"image","len":len(questions1)})

    if questions1[i].question_type=="Single Image":
        return render(request,"image.html",
        {"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})

    if questions1[i].question_type=="Multiple Image":
        return render(request,"images.html",
        {"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})


def av_test(request,pk,pk1,pk2,pk3,pk4):

    questions1 = sorted(av_question.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4),
    key=lambda x: random.random())

    print(questions1,len(questions1))
    data = serializers.serialize('json', questions1)
    print(data)
    request.session['questions'] = data
    module1=program_module.objects.get(pk=pk3)
    level1=module_level.objects.get(pk=pk4)
    i=-1
    return render(request,"av_test.html",
    {"q":questions1,"score":0,"i":i,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4,"m":module1,"l":level1})

def ajax_av_test(request,pk,pk1,pk2,pk3,pk4):
    questionss = request.session.get('questions')
    questions1=[]
    for copy in serializers.deserialize("json", questionss):
        questions1.append(copy.object)
    print("QUERUBOI",questions1)
    i = int(request.GET.get('id'))
    c = (request.GET.get('correct'))
    s = int(request.GET.get('score'))
    ques=av_sub_question.objects.filter(av=questions1[i].pk)
    i+=1
    if i==len(questions1):
        count=0
        for i in questions1:
            ques=av_sub_question.objects.filter(av=i.pk)
            count+=len(ques)

        return render(request,"test_submit.html",
        {"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4,"test_name":"av","len":count})

    if questions1[i].question_type=="Video":
        ques=av_sub_question.objects.filter(av=questions1[i].pk)
        return render(request,"video.html",
        {"q":questions1,"q1":ques,"i":i,"r":range(0,len(ques)),"l":len(ques),"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})

    if questions1[i].question_type=="Audio":
        ques=av_sub_question.objects.filter(av=questions1[i].pk)
        return render(request,"audio.html",
        {"q":questions1,"q1":ques,"i":i,"r":range(0,len(ques)),"l":len(ques),"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})



from datetime import datetime

def test_submit(request,pk,pk1,pk2,pk3,pk4):
    student1=student.objects.get(pk=pk)
    program1=program.objects.get(pk=pk2)
    module1=program_module.objects.get(pk=pk3)
    level1=module_level.objects.get(pk=pk4)
    batch1=batch.objects.get(pk=pk1)
    test_name = request.GET.get('test_name')
    print(test_name)
    if test_name=="standard":
        s=student_status(student_id=student1,program_id=program1,module_id=module1,level_id=level1,batch_id=batch1,
        date_time=datetime.now(),status="S_Pass",score=int(request.GET.get('score')))
        s.save()
    if test_name=="image":
        s=student_status(student_id=student1,program_id=program1,module_id=module1,level_id=level1,batch_id=batch1,
        date_time=datetime.now(),status="I_Pass",score=int(request.GET.get('score')))
        s.save()
    if test_name=="av":
        s=student_status(student_id=student1,program_id=program1,module_id=module1,level_id=level1,batch_id=batch1,
        date_time=datetime.now(),status="AV_Pass",score=int(request.GET.get('score')))
        s.save()

    return render(request,"dummy.html")
