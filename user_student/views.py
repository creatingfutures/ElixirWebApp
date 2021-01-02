from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import student_status
import json
from django.core import serializers
from user_admin.models import entity, entity_type, entity_status
from user_admin.models import student, facilitator, program, center
from user_admin.models import batch, program_module, module_level,question_option, question, student_module_level, student_batch,question_content,question_type
# from user_admin.models import image_question,images_question, av_question,av_sub_question
from user_student.models import scores,student_status
import random
import os
import json
import datetime
from .crossword_puzzle import Crossword


def login(request):
    batches = batch.objects.all()
    if request.method == "POST":
        search_query1 = request.POST.get('student', None)
        search_query2 = request.POST.get('batch', None)
        try:
            stud = student.objects.get(pk=int(search_query1))
        except:
            messages.success(request, f'No student of that ID exists')
            return redirect("student_login")
        return redirect('s_home', search_query1, search_query2)
    return render(request, "student_login.html", {"b": batches})


def s_home(request, pk, pk1):
    programs = program.objects.all()
    stud = student.objects.get(student_id=pk)
    return render(request, 's_home.html', {"p1": programs, "pk": pk, "pk1": pk1, "s": stud})



def spoken_english(request, pk, pk1, pk2):
    if pk2 == 3:
        modules = program_module.objects.filter(program_id=pk2)
        program1 = program.objects.get(pk=pk2)
        levels=[]
        for i in modules:
            levels.append(module_level.objects.filter(
            module_id=i.module_id).order_by('level_description'))
    
        return render(request, "e2e.html", {"m": modules, "pk": pk, "pk1": pk1, "pk2": pk2, "p": program1,"l":zip(modules,levels)})
    else:
     
        modules = program_module.objects.filter(program_id=pk2)
        if pk2 == 3:
            order = [4, 1, 0, 7, 3, 2, 6, 5]
            modules = [modules[i] for i in order]
            
        program1 = program.objects.get(pk=pk2)
        levels= []
        questiontypes = []
        questiontypesList = []
        for i in modules:
            questiontypes = []
            level_Ids = module_level.objects.filter(module_id=i.module_id).order_by('level_id')
            if len(level_Ids) > 0:
                for level_Id in level_Ids:
                    questiontypes = []
                    questiontype_Ids = question.objects.filter(level_id=level_Id.level_id).order_by('question_type_id').distinct()
                    if questiontype_Ids != None: 
                        for questiontype in questiontype_Ids:
                            questionType = question_type.objects.get(pk = questiontype.question_type_id)
                            questiontypes.append(questionType.question_type)
                       # questiontypesList = [questiontypesList[i] for i in [12,1,2]]
                        questiontypesList.append({ 'level_id' :level_Id.level_id, 'questiontypes': set(dict.fromkeys(questiontypes)) })
            levels.append({ 'level' :module_level.objects.filter(
            module_id=i.module_id).order_by('level_description', 'level_id')})
        return render(request, "spoken_english.html", {"m": modules, "pk": pk, "pk1": pk1, "pk2": pk2, "p": program1,"l":zip(modules,levels),"q_t":questiontypesList})

          
def e2e_modules(request, pk, pk1, pk2, pk3, pk4):
    module = program_module.objects.get(pk=pk3)
    if pk3 == 20:
       level = module_level.objects.get(pk=pk4)
       return render(request, "resume_builder/index.html", {"m": module, "l": level, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3})
    else:
         level = module_level.objects.get(pk=pk4)
         return redirect('standard_test',pk,pk1,pk2,pk3,pk4)   

def module_view(request, pk, pk1, pk2, pk3):
    levels = module_level.objects.filter(
        module_id=pk3).order_by('level_description')
    module = program_module.objects.get(module_id=pk3)
    return render(request, "module_view.html", {"l": levels, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "m": module, "g": 'https://www.google.com'})


def level_view(request, pk, pk1, pk2, pk3, pk4):
    question_types = ['Assessment', 'Image Test ', 'Audio / Video Test',
                      'CrossWord', 'Word Search']
    level = module_level.objects.get(level_id=pk4)
    return render(request, "level_view.html", {"question_types": question_types, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, 'pk4': pk4, "l": level})

def word_find(request,pk,pk1,pk2,m,l,narrative):
    QandA = question_option.objects.all() # Querying all the questions
    QUEST = [] # list to store the required questions
    ANS = [] # list to store the respective answers
    level = module_level.objects.get(pk=l) 
    module = program_module.objects.get(pk=m)
    for i in QandA:
        if( (i.question.level==level and i.question.level.module == module) and (i.question.question_type.question_type_id==11 and i.question.narrative == narrative)): 
            ANS.append(i.option_description)    
    return render(request,"wordsearch/wordfind.html",{"pk":pk,"pk1":pk1,"pk2":pk2,"m":module,"l":level,'ans':ANS,'typ':11,'narrative':narrative})


def list_narrative(request,pk,pk1,pk2,m,l,question_type_id): # returns hyperlinks which contains questions related to specify narratives
    level = module_level.objects.get(pk=l)
    module = program_module.objects.get(pk=m)
    Qj = question.objects.filter(level=level,question_type_id=question_type_id) # making sure we are queryting match the following quetions
    narratives = [] # all narratives related to match the following
    distinct_narratives = [] # removed repeating narratives
    for i in Qj:
        narratives.append(i.narrative)
    for i in narratives:
        if i not in distinct_narratives:
            distinct_narratives.append(i)
    name = question_type.objects.get(question_type_id=question_type_id)
    return render(request,"all_hyperlinks.html",{"pk":pk,"pk1":pk1,"pk2":pk2,"m":module,"l":level,'d':distinct_narratives,'name':name})

def score_save(request,pk,pk1,pk2,m,l,typ,score,total_score):
    level_id = module_level.objects.get(level_id = l)
    batch_id = batch.objects.get(batch_id = pk1)
    module_id = program_module.objects.get(module_id = m)
    student_id = student.objects.get(student_id = pk)
    date_time = datetime.datetime.now() # get present time
    assessment_type = ''
    pass_status = True
    total_score = total_score
    if(typ == 2): #GA
        try:
            student_query = scores.objects.get(student_id=pk,assesment_type='GA',level_id=level_id)
        except scores.DoesNotExist:
            student_query = None
        if(student_query==None):
            assessment_type = 'GA'
            obj = scores.objects.create(assesment_type=assessment_type,student_id=student_id,batch_id=batch_id,level_id=level_id,user_score = score,total_score = total_score,date_time = date_time)
            obj.save()
        else:
            student_query.user_score = score
            student_query.date_time = datetime.datetime.now()
            student_query.save()
    if request.method == 'POST':
        if int(request.POST.get('user_score',False))>0:
            pass_status = True
        else:
            pass_status = False
    if(typ==1):
        if(pass_status):
            total_score = 1
            user_score = 1
        else:
            total_score = 1
            user_score = 0
    if(typ==11 or typ==1):
        assessment_type = request.POST.get('assessment_type',False)
        try:
            student_query = scores.objects.get(student_id=pk,assesment_type=assessment_type,level_id=level_id)
        except scores.DoesNotExist:
            student_query = None
        if(student_query==None):
            obj = scores.objects.create(assesment_type=assessment_type,student_id=student_id,batch_id=batch_id,level_id=level_id,user_score = score,total_score = total_score,date_time = date_time)
            obj.save()
        else:
            student_query.level_id = level_id
            student_query.user_score = score
            student_query.date_time = datetime.datetime.now()
            student_query.save()   
    return render(request,"score_card.html",{'score':request.POST.get('user_score',False),"pk":pk,"pk1":pk1,"pk2":pk2,"m":m,"l":l,'assessment_type':assessment_type,'pass_status':pass_status,'typ':typ})


def match(request,pk,pk1,pk2,m,l,narrative):
    QandA = question_option.objects.all() # Querying all the questions
    QUEST = [] # list to store the required questions
    ANS = [] # list to store the respective answers
    level = module_level.objects.get(pk=l) 
    module = program_module.objects.get(pk=m)
    for i in QandA:
        if( (i.question.level==level and i.question.level.module == module) and (i.question.question_type.question_type_id==1 and i.question.narrative == narrative)):
            QUEST.append(i.question.question) 
            ANS.append(i.option_description)
    options = random.sample(range(0,len(QUEST)),len(QUEST)) # randomising options
    print(QUEST,ANS)
    rans = [] # randomising answers
    final_options = [] # correct answers after randomising
    for i in range(0,len(QUEST)):
        rans.append(ANS[options[i]])
    for i in range(0,len(QUEST)):
        for j in range(0,len(QUEST)):
            if(ANS[i]==rans[j]):
                final_options.append(j+1)
    typ = 1
    two_cols = dict(zip(QUEST,rans))
    return render(request,"match/match25.html",{"pk":pk,"pk1":pk1,"pk2":pk2,"m":module,"l":level,"typ":typ,'cola':rans,'colq':QUEST,'two_cols':two_cols,'final_options':final_options,'narrative':narrative})
    #"match/match%s.html" %l


def crossword(request, pk, pk1, pk2, m, l):
    
    module = program_module.objects.get(pk=m)
    level = module_level.objects.get(pk=l)
    return render(request,"crossword/crossword.html",{"pk":pk,"pk1":pk1,"pk2":pk2,"m":module,"l":level})
    
def lesson(request, pk, pk1, pk2, pk3, pk4):
     str1 = "help"
     module = program_module.objects.get(pk=pk3)
     program1 = program.objects.get(pk=pk2)
     level = module_level.objects.get(pk=pk4)
     str1 = str1+"/"+program1.program_name
     str1 = str1+"/"+module.module_name
     str1 = str1+"/"+str(level.level_description)
     str1 = str1+".html"
     
     
     return render(request, str1 ,{"pk":pk,"pk1":pk1,"pk2":pk2})
    

def before_test(request, pk, pk1, pk2, pk3, pk4):
    module1 = program_module.objects.get(pk=pk3)
    level1 = module_level.objects.get(pk=pk4)
    return render(request, "before_test.html",
                  {"pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4, "m": module1, "l": level1})


def trimQuestions(ques):
    ques.question = ques.question.strip()
    return ques

def standard_test(request, pk, pk1, pk2, pk3, pk4):
    questions1= sorted(question.objects.filter(level_id=pk4,question_type_id__in=[2,12,3,4,5,6]).order_by('-pk'),key=lambda x: random.random())[:20]
    result = list(map(trimQuestions,questions1))
    data = serializers.serialize('json', result)
    request.session['questions'] = data
    module1 = program_module.objects.get(pk=pk3)
    level1 = module_level.objects.get(pk=pk4)
    i = -1
    return render(request, "standard_test.html",
                  { "score": 0, "i": i, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4, "m": module1, "l": level1})


def ajax_standard_test(request, pk, pk1, pk2, pk3, pk4):
    questionss = request.session.get('questions')
    questions1 = []
    for copy in serializers.deserialize("json", questionss):
        questions1.append(copy.object)
    i = int(request.GET.get('id'))
    c = (request.GET.get('correct'))
    s = int(request.GET.get('score'))
    if c == "True":
        s = s+1
    elif c == "False":
        s = s+0
    i += 1
    if i == len(questions1):
        score = s
        typ = 2
        total_score = 20
        score_save(request,pk,pk1,pk2,pk3,pk4,typ,score,total_score)
        return render(request, "test_submit.html",
                      {"i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4, "test_name": "standard", "len": len(questions1)})

    if questions1[i].question_type.question_type == "Multiple Choice":
        return render(request, "mcq.html",
                      {"i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})

    if questions1[i].question_type.question_type == "Fill in the blanks":
        return render(request, "fill_ups.html",
                      {"i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})

    if questions1[i].question_type.question_type == "Riddles":
        return render(request, "riddles.html",
                      {"i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})
    if questions1[i].question_type.question_type == "Multiple image based question":
        return render(request, "images.html",
                      {"i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})
    if questions1[i].question_type.question_type == "Single image based question":
        return render(request, "image.html",
                      { "i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})
    # if questions1[i].question_type.question_type == "Audio":
    #     ques = question_content.objects.filter(question_content_id=questions1[i].question_content_id)
    #     return render(request, "audio.html",
    #                   {"q": questions1, "q1": ques, "i": i, "r": range(0, len(ques)), "l": len(ques), "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})
    if questions1[i].question_type.question_type == "Unscramble":
        str = questions1[i].question
        print(str.split())
        return render(request, "jumbled_words.html",
                      {"len": range(0, len(str.split())), "words": str.split(),
                       "i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})

   
def image_test(request, pk, pk1, pk2, pk3, pk4):
    return redirect("error")

#     questions1 = []

#     images = sorted(images_question.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4).order_by('-pk'),
#                     key=lambda x: random.random())
#     questions1 += images

#     image = sorted(image_question.objects.filter(program_id=pk2).filter(module_id=pk3).filter(level_id=pk4).order_by('-pk'),
#                    key=lambda x: random.random())
#     questions1 += image

#     print(questions1, len(questions1))
#     data = serializers.serialize('json', questions1)
#     print(data)
#     request.session['questions'] = data
#     module1 = program_module.objects.get(pk=pk3)
#     level1 = module_level.objects.get(pk=pk4)
#     i = -1
#     return render(request, "image_test.html",
#                   {"q": questions1, "score": 0, "i": i, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4, "m": module1, "l": level1})


def ajax_image_test(request, pk, pk1, pk2, pk3, pk4):
    return redirect("error")

#     questionss = request.session.get('questions')
#     questions1 = []
#     for copy in serializers.deserialize("json", questionss):
#         questions1.append(copy.object)
#     print("QUERUBOI", questions1)
#     i = int(request.GET.get('id'))
#     c = (request.GET.get('correct'))
#     s = int(request.GET.get('score'))
#     if c == "True":
#         s = s+1
#     elif c == "False":
#         s = s+0
#     i += 1
#     if i == len(questions1):
#         return render(request, "test_submit.html",
#                       {"q": questions1, "i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4, "test_name": "image", "len": len(questions1)})

#     if questions1[i].question_type == "Single Image":
#         return render(request, "image.html",
#                       {"q": questions1, "i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})

#     if questions1[i].question_type == "Multiple Image":
#         return render(request, "images.html",
#                       {"q": questions1, "i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4})


def av_test(request, pk, pk1, pk2, pk3, pk4,pk5):
    questions1 = question.objects.filter(level_id=pk4).filter(question_type_id=pk5).order_by('-question_content_id')              
    print(questions1, len(questions1))
    data = serializers.serialize('json', questions1)
    #print(data)
    request.session['questions'] = data
    module = program_module.objects.get(pk=pk3)
    level = module_level.objects.get(pk=pk4)
    i = 0
    return render(request, "av_test.html",{"q": questions1, "score": 0, "i": i, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,"pk5":pk5, "m": module, "l": level})


def ajax_av_test(request, pk, pk1, pk2, pk3, pk4,pk5):
    questionss = request.session.get('questions')
    questions1 = []
    for copy in serializers.deserialize("json", questionss):
        questions1.append(copy.object)
    print("QUERUBOI", questions1)
    i = int(request.GET.get('id'))
    c = (request.GET.get('correct'))
    s = int(request.GET.get('score'))
    
     
    if c == "True":
        s = s+1
    elif c == "False":
        s = s+0
    
    
    j=len(questions1)
    #print(questions1[i].question_type)
    if i >= j:
            i=j
            return render(request, "test_submit.html",
                      {"q": questions1, "i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4, "pk5":pk5,"test_name": "av_test", "len": len(questions1)})
    if questions1[i].question_type.question_type == "Video":
        ques = question.objects.filter(question_content_id=questions1[i].question_content_id)
        return render(request, "video.html",
                      {"q": questions1, "q1": ques, "i": i, "r": range(0, len(ques)), "l": len(ques), "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,"pk5":pk5})

    if questions1[i].question_type.question_type == "Audio":
        
        ques = question.objects.filter(question_content_id=questions1[i].question_content_id)
        # a = ques[i].question_content_id
        print(i)
        return render(request, "audio.html",
                      {"q": questions1, "q1": ques, "i": i, "r": range(0, len(ques)), "l": len(ques), "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,"pk5":pk5})
    if questions1[i].question_type.question_type == "Text":
        
        ques = question.objects.filter(question_content_id=questions1[i].question_content_id)
        # a = ques[i].question_content_id
        print(i)
        return render(request, "text.html",
                      {"q": questions1, "q1": ques, "i": i, "r": range(0, len(ques)), "l": len(ques), "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,"pk5":pk5})


def test_submit(request, pk, pk1, pk2, pk3, pk4):
    student1 = student.objects.get(pk=pk)
    program1 = program.objects.get(pk=pk2)
    module1 = program_module.objects.get(pk=pk3)
    level1 = module_level.objects.get(pk=pk4)
    batch1 = batch.objects.get(pk=pk1)
    test_name = request.GET.get('test_name')
    print(test_name)
    if test_name == "standard":
        s = student_status(student_id=student1, program_id=program1, module_id=module1, level_id=level1, batch_id=batch1,
                           date_time=datetime.now(), status="S_Pass", score=int(request.GET.get('score')))
        s.save()
    if test_name == "image":
        s = student_status(student_id=student1, program_id=program1, module_id=module1, level_id=level1, batch_id=batch1,
                           date_time=datetime.now(), status="I_Pass", score=int(request.GET.get('score')))
        s.save()
    if test_name == "av":
        s = student_status(student_id=student1, program_id=program1, module_id=module1, level_id=level1, batch_id=batch1,
                           date_time=datetime.now(), status="AV_Pass", score=int(request.GET.get('score')))
        s.save()

    return render(request, "dummy.html")
