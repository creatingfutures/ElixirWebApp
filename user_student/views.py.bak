from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
#from .models import student_status
import json
from django.core import serializers
from user_admin.models import entity, entity_type, entity_status
from user_admin.models import student, facilitator, program, center
from user_admin.models import batch, program_module, module_level,question_option, question, student_module_level, student_batch,question_content,question_type,assessment_type
# from user_admin.models import image_question,images_question, av_question,av_sub_question
from user_student.models import scores
import random
import os
import json
import datetime
from .crossword_puzzle import Crossword
from django.db.models import Sum


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


def spoken_english(request, pk, pk1, programName):

    programObj=program.objects.filter(program_name=programName)
    programId = 0
    if len(programObj)>0:
        programId=programObj[0].program_id
    else:
         return render(request,'error.html',{"pk": pk, "pk1": pk1})
    program_modules = program_module.objects.filter(program_id=programId)
    print("modules")
    print(program_modules)
    program_module_ids = [module.module_id for module in program_modules];
    program_levels= module_level.objects.filter(module_id__in=program_module_ids)
   # for i in modules:
       #levels.append(module_level.objects.filter(module_id=i.module_id).order_by('level_description'))
    print ("levels")
    print(program_levels)
    program_level_ids= [level.level_id for level in program_levels]
    program_scores = scores.objects.filter(student_id=pk,batch_id=pk1,level_id__in=program_level_ids).all()
    question_type_name = str(assessment_type.objects.get(assessment_type='General Assessment'))
    #print(question_type_name)
    assesment_type_in_scores = [score.assessment_type_id for score in program_scores ]
    levels_in_scores = [score.level_id for score in program_scores]
    F = []
    all_scores={}
    scores_level={}
    scores_module={}
    scores_level_keys=[score.level_id.module.module_name +'-'+score.level_id.level_description  for score in program_scores]
    scores_module_keys=[score.level_id.module.module_name for score in program_scores]

    all_scores = {str(score.level_id.module.module_name)+'-'+str(score.level_id.level_description)+'-'+str(score.assessment_type_id.assessment_type) : round( ((score.user_score/score.total_score)*100),2) for score in program_scores}
    scores_level = {}
    for lvl_key in scores_level_keys:
        level_scores = [value for key, value in all_scores.items() if lvl_key.lower() in key.lower()]
        all_scores[lvl_key]= round( (sum(level_scores)/len(level_scores)),2)
    for module_key in scores_module_keys:
        module_scores = [value for key, value in all_scores.items() if module_key.lower() in key.lower()]
        all_scores[module_key]= round((sum(module_scores)/len(module_scores)),2)
    if programName.lower() == "education to employability":
        return render(request, "spoken_english.html", {"m": program_modules, "pk": pk, "pk1": pk1, "pk2": programId, "p": programObj,"l":program_levels,'scores':all_scores})
    else:

       # modules = program_module.objects.filter(program_id=programId)    
        if len(program_modules)>0:
           return render(request, "spoken_english.html", {"m": program_modules, "pk": pk, "pk1": pk1, "pk2": programId, "p": programObj,"l": program_levels,'scores':all_scores})
        else:
            return render(request,'error.html',{"pk": pk, "pk1": pk1})
          
def resumebuilder(request, pk, pk1, pk2, pk3, pk4):
    module = program_module.objects.get(pk=pk3)
    if module.module_name.lower() == 'resume builder':
       level = module_level.objects.get(pk=pk4)
       return render(request, "resume_builder/index.html", {"m": module, "l": level, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3})
    else:
       return render(request,'error.html',{"pk": pk, "pk1": pk1})

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

def word_find(request,pk,pk1,pk2,m,l,narrative,assessment_type_id):
    QandA = question_option.objects.all() # Querying all the questions
    QUEST = [] # list to store the required questions
    ANS = [] # list to store the respective answers
    level = module_level.objects.get(pk=l) 
    module = program_module.objects.get(pk=m)
    question_content_id = 0
    q_type = question.objects.filter(assessment_type_id=assessment_type_id)[0].question_type
    for i in QandA:
        if( (i.question.level==level and i.question.level.module == module) and (i.question.question_type== q_type and i.question.narrative == narrative)): 
            ANS.append(str(i.option_description).replace(' ',''))
            if(question_content_id==0):
                question_content_id= i.question.question_id
    typ = assessment_type_id 
    return render(request,"wordsearch/wordfind.html",{"pk":pk,"pk1":pk1,"pk2":pk2,"m":module,"l":level,'ans':ANS,'typ':typ,'narrative':narrative,'question_content_id':question_content_id})


def list_narrative(request,pk,pk1,pk2,m,l,assessment_type_id): # returns hyperlinks which contains questions related to specify narratives
    print('list_narrative',assessment_type_id)
    level = module_level.objects.get(pk=l)
    module = program_module.objects.get(pk=m)
    assess_name = assessment_type.objects.get(assessment_type_id=assessment_type_id)
    print(assess_name)
    Qj = question.objects.filter(level=level,assessment_type=assessment_type_id) # making sure we are queryting match the following quetions
    print(Qj)
    narratives = [] # all narratives related to match the following
    distinct_narratives = [] # removed repeating narratives
    for i in Qj:
        narratives.append(i.narrative)
    for i in narratives:
        if i not in distinct_narratives and i!=None:
            distinct_narratives.append(i)
    
    print(assess_name,assessment_type_id)
    return render(request,"all_hyperlink.html",{"pk":pk,"pk1":pk1,"pk2":pk2,"m":module,"l":level,'d':distinct_narratives,'assessment_type':assess_name,'assessment_type_id':assessment_type_id})

def score_save(request,pk,pk1,pk2,m,l,typ,score,total_score):
    level_id = module_level.objects.get(level_id = l)
    batch_id = batch.objects.get(batch_id = pk1)
    module_id = program_module.objects.get(module_id = m)
    student_id = student.objects.get(student_id = pk)
    date_time = datetime.datetime.now() # get present time
    pass_status = True
    total_score = total_score
    question_content_id = request.POST.get('question_content_id')
    narrative = request.POST.get('narrative')
    q_type = assessment_type.objects.get(assessment_type_id=typ)
    if(score==0):
        pass_status= False
    if(str(q_type.assessment_type).lower()=='text test' or str(q_type.assessment_type).lower()=='video' or str(q_type.assessment_type).lower()=='audio'):
        question_content_id = request.session.get('question_content_id')
        score_save_helper(student_id,q_type.assessment_type,level_id,batch_id,pass_status,score,total_score,question_content_id,request.session.get('narrative'),typ)
    else:
        if(str(q_type.assessment_type).lower() == 'general assessment'): #GA
            score_save_helper(student_id,q_type.assessment_type,level_id,batch_id,pass_status,score,total_score,0,'narrative',typ)  
        else:
            score_save_helper(student_id,q_type.assessment_type,level_id,batch_id,pass_status,score,total_score,question_content_id,narrative,typ)
    return render(request,"score_card.html",{'score':request.POST.get('user_score',0),"pk":pk,"pk1":pk1,"pk2":pk2,"m":m,"l":l,'narrative':narrative,'pass_status':pass_status,'typ':typ,'question_type':str(q_type.assessment_type).lower()})
   
def score_save_helper(student_id,question_type_name,level_id,batch_id,pass_status,score,total_score,question_content_id,narrative,typ):
        try:
            if(str(question_type_name).lower()=='general assessment'):
                assessment_type_id = assessment_type.objects.get(assessment_type__iexact=str(question_type_name).lower())
                student_query = scores.objects.get(batch_id=batch_id,student_id=student_id,level_id=level_id,assessment_type_id=assessment_type_id)
                print('a1')
            elif(str(question_type_name).lower()=='text test' or str(question_type_name).lower()=='audio' or str(question_type_name).lower()=='video' ):
                assessment_type_id=assessment_type.objects.get(assessment_type__iexact=str(question_type_name).lower())
                print(assessment_type_id)
                student_query = scores.objects.get(batch_id=batch_id,student_id=student_id,level_id=level_id,question_content_id=question_content_id)
            else:
                student_query = scores.objects.get(batch_id=batch_id,student_id=student_id,level_id=level_id,question_content_id=question_content_id)
                print('a3')
        except scores.DoesNotExist:
            student_query = None
            print('a4')
        if(student_query==None):
            if(str(question_type_name).lower()=='general assessment'):
                print('a5')
                assessment_type_id = assessment_type.objects.get(assessment_type__iexact=str(question_type_name).lower())
                obj = scores.objects.create(student_id=student_id,batch_id=batch_id,level_id=level_id,user_score = score,total_score = total_score,date_time = datetime.datetime.now(),assessment_type_id=assessment_type_id,question_content_id=question_content_id)
                obj.save()
            elif(str(question_type_name).lower()=='text test' or str(question_type_name).lower()=='audio' or str(question_type_name).lower()=='video' ):
                assessment_type_id=assessment_type.objects.get(assessment_type__iexact=str(question_type_name).lower())
                print(assessment_type_id)
                obj = scores.objects.create(student_id=student_id,batch_id=batch_id,level_id=level_id,user_score = score,total_score = total_score,date_time = datetime.datetime.now(),question_content_id=question_content_id,assessment_type_id=assessment_type_id)
                obj.save()
            else:
                print('a7')
                print('jk',question_type_name)
                assessment_type_id = assessment_type.objects.get(assessment_type__iexact=str(question_type_name).lower())
                obj = scores.objects.create(student_id=student_id,batch_id=batch_id,level_id=level_id,user_score = score,total_score = total_score,date_time = datetime.datetime.now(),question_content_id=question_content_id,assessment_type_id=assessment_type_id)
                obj.save()
        else:
            if(str(question_type_name).lower()=='general assessment'):
                print('a8')
                student_query.user_score = score
                student_query.date_time = datetime.datetime.now()
                student_query.level_id = level_id
                student_query.total_score = total_score
                print(student_query)
                student_query.save()
            elif(str(question_type_name).lower()=="text test" or str(question_type_name).lower()=='audio' or str(question_type_name).lower()=='video'):
                print('a9')
                student_query.user_score = score
                student_query.date_time = datetime.datetime.now()
                student_query.level_id = level_id
                student_query.total_score = total_score
                student_query.question_content_id = question_content_id
                student_query.save()   
            else:
                print('a10')
                print(question.objects.get(question_id=question_content_id).narrative,narrative)
                if( question.objects.get(question_id=question_content_id).narrative == narrative ):
                    print('inside')
                    student_query.user_score = score
                    student_query.date_time = datetime.datetime.now()
                    student_query.level_id = level_id
                    student_query.total_score = total_score
                    student_query.save()    



def match(request,pk,pk1,pk2,m,l,narrative,assessment_type_id):
    print('match',narrative)
    QandA = question_option.objects.all() # Querying all the questions
    QUEST = [] # list to store the required questions
    ANS = [] # list to store the respective answers
    level = module_level.objects.get(pk=l) 
    module = program_module.objects.get(pk=m)
    question_content_id = 0
    q_type = question.objects.filter(assessment_type_id=assessment_type_id)[0].question_type
    print('1',q_type)
    for i in QandA:
        if( (i.question.level==level and i.question.level.module == module) and (i.question.question_type== q_type and i.question.narrative == narrative)):
            QUEST.append(i.question.question) 
            ANS.append(i.option_description)
            if(question_content_id==0):
                question_content_id= i.question.question_id
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
    typ = assessment_type_id
    two_cols = dict(zip(QUEST,rans))
    return render(request,"match/match25.html",{"pk":pk,"pk1":pk1,"pk2":pk2,"m":module,"l":level,"typ":typ,'cola':rans,'colq':QUEST,'two_cols':two_cols,'final_options':final_options,'question_content_id':question_content_id,'narrative':narrative})
    #"match/match%s.html" %l


def crossword(request, pk, pk1, pk2, m, l,narrative,assessment_type_id):
    module = program_module.objects.get(pk=m)
    level = module_level.objects.get(pk=l)
    QandA = question_option.objects.all() # Querying all the questions
    QUEST = [] # list to store the required questions
    ANS = [] # list to store the respective answers
    level = module_level.objects.get(pk=l) 
    module = program_module.objects.get(pk=m)
    question_content_id = 0
    q_type = question.objects.filter(assessment_type_id=assessment_type_id)[0].question_type
    for i in QandA:
        if( (i.question.level==level and i.question.level.module == module) and (i.question.question_type== q_type and i.question.narrative == narrative)): 
            QUEST.append(i.question.question)
            ANS.append(i.option_description)
            if(question_content_id==0):
                question_content_id= i.question.question_id
    word_list=[]
    for i in range(0,len(ANS)):
        c = []
        c.append(str(ANS[i]))
        c.append(str(QUEST[i]))
        word_list.append(c) 
    a = Crossword(13, 13, '0', 5000, word_list)
    a.compute_crossword(2)
    items = a.solution()
    a.display()
    legend,cords,across_or_down,answers,answers_box,word_number = a.legend()
    items = items.replace(' ','')
    items = list(items.replace('\n',''))
    nd_array = []
    arr = []
    n = 0
    for i in items:
        if(n<13):
            arr.append(i)
            n = n+1
        if(n==13):
            nd_array.append(arr)
            n=0
            arr=[]
    items = items
    answer_start = []
    answer_start_index = []
    length_cords = len(cords) 
    for i in cords:
        ans = []
        ans.append(i[1])
        ans.append(i[0])
        answer_start_index.append(ans)
        answer_start_id = 'txt'+'_'+str(i[1])+'_'+ str(i[0])
        answer_start.append(answer_start_id)
    new_cells_allowed=[]
    for i in range(0,length_cords):
        cells_allowed=[]
        if(across_or_down[i]=='across'):
            for j in range(answer_start_index[i][1],answer_start_index[i][1]+answers[i].length):
                rows_allowed = []
                rows_allowed.append(answer_start_index[i][0])
                rows_allowed.append(j)
                cells_allowed.append(rows_allowed)
            new_cells_allowed.append(cells_allowed)
        else:
            for j in range(answer_start_index[i][0],answer_start_index[i][0]+answers[i].length):
                rows_allowed = []
                rows_allowed.append(j)
                rows_allowed.append(answer_start_index[i][1])
                cells_allowed.append(rows_allowed)
            new_cells_allowed.append(cells_allowed)    
    ans = []
    for i in answers:
        ans.append(str(i))
    typ = assessment_type_id
    return render(request,"crossword/crossword.html",{"pk":pk,"pk1":pk1,"pk2":pk2,"m":module,"l":level,'nd_array':nd_array,'legend':legend,'cords':cords,'across_or_down':across_or_down,'items':items,'answer_start':answer_start,'answer_start_index':answer_start_index,'answers':ans,'new_cells_allowed':new_cells_allowed,'typ':typ,'narrative':narrative,'questions':answers_box,'question_content_id':question_content_id,'word_number':word_number})
    
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
        typ = assessment_type.objects.get(assessment_type__iexact='general assessment').assessment_type_id
        total_score = len(questions1)
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
        strs = questions1[i].question
        print(strs.split())
        return render(request, "jumbled_words.html",
                      {"len": range(0, len(strs.split())), "words": strs.split(),
                       "i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,'hint': 'none' if questions1[i].hint == '' else questions1[i].hint})

   
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

#pk,pk1,pk2,m,l,narrative,question_type_id
def av_test(request, pk, pk1, pk2, pk3, pk4,pk5,narrative):
    print(pk, pk1, pk2, pk3, pk4,pk5,narrative)
    print('hi0',type(narrative),narrative)
    questions1 = question.objects.filter(level_id=pk4).filter(assessment_type=assessment_type.objects.get(assessment_type_id=pk5)).filter(narrative=narrative).order_by('-question_content_id')              
    print('questions1',questions1)
    question_content_id = 0
    for i in questions1:
        if(question_content_id==0):
            question_content_id = i.question_content.question_content_id
            request.session['question_content_id'] = i.question_content.question_content_id
            #print('question_content_id my fen',i.question_content.question_content_id)
    print('hi',questions1, len(questions1))
    data = serializers.serialize('json', questions1)
    #print(data)
    request.session['questions'] = data
    request.session['question_content_id'] = question_content_id
    request.session['narrative'] = narrative
    module = program_module.objects.get(pk=pk3)
    level = module_level.objects.get(pk=pk4)
    i = 0
    return render(request, "av_test.html",{ "score": 0, "i": i, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,"pk5":pk5, "m": module, "l": level,'narrative':narrative})


def ajax_av_test(request, pk, pk1, pk2, pk3, pk4,pk5,narrative):
    print('ajax_av_test')
    questionss = request.session.get('questions')
    questions1 = []
    for copy in serializers.deserialize("json", questionss):
        questions1.append(copy.object)
    print("QUERUBOI", questions1)
    i = int(request.GET.get('id'))
    c = (request.GET.get('correct'))
    s = int(request.GET.get('score'))
    print(i,c,s)
    request.session['score']=s
    j=len(questions1)
    if c=='av':
            i=j
            print('total_score fren',j)
            total_score = question.objects.filter(narrative=narrative).count()
            score_save(request,pk,pk1,pk2,pk3,pk4,pk5,s,total_score)
            return render(request, "test_submit.html",
                      { "i": i, "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4, "pk5":pk5,"test_name": "av_test", "len": len(questions1),"narrative":narrative})
    question_content = questions1
    #question_content = question.objects.filter(question_content_id=questions1[0].question_content_id)
    print('---question_content',question_content)
    request.session['question_content']= serializers.serialize('json', question_content)
    print('question_content',request.session['question_content'])
    if questions1[i].question_type.question_type == "Video":
        request.session['question_type'] = questions1[i].question_type.question_type
       # request.session['question_content_id'] = question.objects.filter(question_content_id=questions1[i].question_content_id)
        return render(request, "video.html",{"i": i, "r": range(0, len(question_content)), "l": len(question_content), "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,"pk5":pk5,"narrative":narrative})

    if questions1[i].question_type.question_type == "Audio":
        print('Audio')
        request.session['question_type'] = questions1[i].question_type.question_type
       # request.session['question_content_id'] = question.objects.filter(question_content_id=questions1[i].question_content_id)
        # a = ques[i].question_content_id
        print(i)
        return render(request, "audio.html",{ "i": i, "r": range(0, len(question_content)), "l": len(question_content), "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,"pk5":pk5,"narrative":narrative})
    if questions1[i].question_type.question_type == "Text":
        request.session['question_type'] = questions1[i].question_type.question_type
        #question_content_id = questions1[i].question_content_id
      #  print('text question_content_id',question_content_id)
        print(i)
        return render(request, "text.html",
                                            {"q1": question_content, "i": i, "r": range(0, len(question_content)), "l": len(question_content), "score": s, "pk": pk, "pk1": pk1, "pk2": pk2, "pk3": pk3, "pk4": pk4,"pk5":pk5,"narrative":narrative})


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
