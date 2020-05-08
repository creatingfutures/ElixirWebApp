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
from user_admin.models import batch,program_module,module_level,questions
from user_admin.models import student_module_level,student_batch


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
    programs=program.objects.get(program_name="Spoken English")
    return render(request,'s_home.html',{"p":programs,"pk":pk,"pk1":pk1})


def spoken_english(request,pk,pk1,pk2):
    modules=program_module.objects.get(program_id=pk2)
    return render(request,"spoken_english.html",{"m":modules,"pk":pk,"pk1":pk1,"pk2":pk2})


def sentances(request,pk,pk1,pk2,pk3):
    levels=module_level.objects.get(level_number=1)
    return render(request,"sentances.html",{"l":levels,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3})


def sentances_level_1_test(request,pk,pk1,pk2,pk3,pk4):
    questions1=questions.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4)
    i=0
    return render(request,"sentances_level_1_test.html",{"q":questions1,"score":0,"i":i,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})

def ajax_check(request,pk,pk1,pk2,pk3,pk4):
    questions1=questions.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4)
    i = int(request.GET.get('id'))
    c = (request.GET.get('correct'))
    s = int(request.GET.get('score'))
    if c=="True":
        s=s+1
    elif c=="False":
        s=s+0
    if i==8:
        return render(request,"sentances_test_submit.html",{"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})

    i+=1

    return render(request,"sentances_test_check.html",{"q":questions1,"i":i,"score":s,"pk":pk,"pk1":pk1,"pk2":pk2,"pk3":pk3,"pk4":pk4})

from datetime import datetime

def sentances_test_submit(request,pk,pk1,pk2,pk3,pk4):
    questions1=questions.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4)
    student1=student.objects.get(pk=pk)
    program1=program.objects.get(pk=pk2)
    module1=program_module.objects.get(pk=pk3)
    level1=module_level.objects.get(pk=pk4)
    batch1=batch.objects.get(pk=pk1)
    s=student_status(student_id=student1,program_id=program1,module_id=module1,level_id=level1,batch_id=batch1,
    date_time=datetime.now(),status="Pass",score=int(request.GET.get('score')))
    s.save()

    return render(request,"dummy.html")
