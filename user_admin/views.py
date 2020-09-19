from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import program, program_module, facilitator, center, student
from .models import module_level, question, question_type, question_content, batch, entity_status
import json
from django.core import serializers
from django import forms
import django
from .forms import *
import re
from django.db.models import Q

# Create your views here.
import csv
program_modules = {}
facilitators = {}
mod_c = 0
fac_c = 0
paginator_num_pages = 10


def error(request):
    return HttpResponse("error")


def student_export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['student_id', 'first_name', 'middle_name', 'last_name',
                     'mobile_number', 'email', 'gender', 'dob', 'address', 'status'])

    for i in student.objects.all().values_list('student_id', 'first_name', 'middle_name', 'last_name', 'mobile_number', 'email_id', 'gender', 'dob', 'address_1', 'status'):
        j = list(i)
        id = j[len(j)-1]
        status = entity_status.objects.get(pk=id)
        j.pop(len(j)-1)
        j.append(status.description)
        writer.writerow(j)

    response['Content-Disposition'] = 'attachment;filename="stuents.csv"'
    return response


def questions_export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['question_id', 'question', 'narrative',
                     'question_type', 'program', 'module', 'level', 'options', 'answer'])

    for i in question.objects.all().values_list('question_id', 'question', 'narrative', 'question_type'):
        i = list(i)
        q = question.objects.get(pk=i[0])
        i.append(q.program)
        i.append(q.module)
        i.append(q.level)
        options = ""
        for j in q.options:
            options += f'<{j}>'
        i.append(options)
        i.append(q.answer)
        writer.writerow(i)

    response['Content-Disposition'] = 'attachment;filename="questions.csv"'

    return response


@login_required
def home(request):
    programs = program.objects.all()
    spok = program.objects.get(program_name="spoken english")
    modules = program_module.objects.filter(program_id=spok)

    facilitators = facilitator.objects.all()
    module_count_dict = {}
    paginator = Paginator(programs, paginator_num_pages)

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    try:
        programs1 = paginator.page(page)
    except:
        programs1 = paginator.page(paginator_num_pages)

    paginator = Paginator(facilitators, paginator_num_pages)
    try:
        page = int(request.GET.get('page2'))
    except:
        page = 1

    try:
        facilitator1 = paginator.page(page)
    except:
        facilitator1 = paginator.page(paginator_num_pages)

    paginator = Paginator(modules, paginator_num_pages)
    try:
        page = int(request.GET.get('page3'))
    except:
        page = 1

    try:
        modules1 = paginator.page(page)
    except:
        modules1 = paginator.page(paginator_num_pages)

    for i in programs:
        module_count = 0
        for j in modules:
            if j.program_id == i.program_id:
                module_count += 1
        module_count_dict[i] = module_count

    a = {"p": programs1,
         "pmc": module_count_dict, "p1": programs, "f": facilitator1, "m": modules1}
    return render(request, 'home.html', a)


def load_modules_home(request):
    program_id = request.GET.get('program_id')
    prog = program.objects.get(program_id=program_id)
    moduless = program_module.objects.all()
    modules = program_module.objects.filter(program_id=program_id)

    paginator = Paginator(moduless, paginator_num_pages)
    try:
        page = int(request.GET.get('page4'))
    except:
        page = 1

    try:
        modules1 = paginator.page(page)
    except:
        modules1 = paginator.page(paginator_num_pages)

    if len(modules) == 0:
        not1 = False
    else:
        not1 = True

    return render(request, 'ajax/module_dropdown_list_home.html', {"mm": modules1, "p": prog, "n": not1, "m11": modules})


def load_fac_home(request):
    fac_id = request.GET.get('facilitator_id')
    facs = facilitator.objects.all()
    fac_list = []
    for i in facs:
        if fac_id.lower() in i.first_name:
            fac_list.append(i)
        elif fac_id.lower() in i.last_name:
            fac_list.append(i)

    paginator = Paginator(facs, paginator_num_pages)
    try:
        page = int(request.GET.get('page2'))
    except:
        page = 1

    try:
        facilitator1 = paginator.page(page)
    except:
        facilitator1 = paginator.page(paginator_num_pages)

    if len(fac_list) == 0:
        not1 = False
    else:
        not1 = True
    return render(request, 'ajax/module_dropdown_fac_home.html', {"m": fac_list, "n": not1, "f": facilitator1})


def add_program(request):
    if request.method == "POST":
        form = add_program_form(request.POST, request.FILES)
        if form.is_valid():
            a = form.cleaned_data.get('program_name')
            form.save()
            messages.success(request, f'Successfully Added {a}')
            return redirect('home')
    else:
        form = add_program_form()

    return render(request, 'add_program.html', {"form": form})


def edit_program(request, pk):
    a = program.objects.get(pk=pk)
    if request.method == "POST":
        form = add_program_form(request.POST, request.FILES, instance=a)
        if form.is_valid():
            a = form.cleaned_data.get('program_name')
            form.save()
            messages.success(request, f'Successfully edited{a}')
            return redirect('home')
    else:
        form = add_program_form(instance=a)

    return render(request, 'add_program.html', {"form": form})


def delete_program(request, pk):
    a = get_object_or_404(program, pk=pk)
    if request.method == "POST":
        q = program.objects.get(pk=pk)
        a1 = q.program_name
        messages.success(request, f'Successfully Deleted {a1}')
        q.delete()
        return redirect('home')

    return render(request, 'delete_program.html', {"a": a})


def add_module(request, pk):
    if request.method == "POST":
        form = add_module_form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.program = program.objects.get(pk=pk)
            module_name = form.cleaned_data.get('module_name')
            form.save()
            messages.success(request, f'Successfully edited {module_name}')
            return redirect('home')
    else:
        form = add_module_form()
    return render(request, 'add_module.html', {"form": form})


def edit_module(request, pk, pk1):
    a = program.objects.get(pk=pk)
    a1 = program_module.objects.get(pk=pk1)
    if request.method == "POST":
        form = add_module_form(request.POST, request.FILES, instance=a1)
        form.instance.program_id = a
        if form.is_valid():
            a = form.cleaned_data.get('module_name')
            form.save()
            messages.success(request, f'Successfully edited {a}')
            return redirect('view_module', pk, pk1)
    else:
        form = add_module_form(instance=a1)
    return render(request, 'add_module.html', {"form": form})


def delete_module(request, pk):
    a = get_object_or_404(program_module, pk=pk)
    if request.method == "POST":
        q = program_module.objects.get(pk=pk)
        a1 = q.module_name
        messages.success(request, f'Successfully Deleted {a1}')
        q.delete()
        return redirect('home')

    return render(request, 'delete_module.html', {"a": a})


def add_level(request, pk, pk1):
    a = program_module.objects.get(pk=pk1)
    if request.method == "POST":
        form = add_level_form(request.POST, request.FILES)
        form.instance.module = a
        if form.is_valid():
            a = form.cleaned_data.get('level_description')
            form.save()
            messages.success(request, f'Successfully added {a}')
            return redirect('view_module', pk, pk1)
    else:
        form = add_level_form()
    return render(request, 'add_level.html', {"form": form})


def edit_level(request, pk, pk1, pk2):
    a = module_level.objects.get(pk=pk2)
    if request.method == "POST":
        form = add_level_form(request.POST, request.FILES, instance=a)
        if form.is_valid():
            a = form.cleaned_data.get('level_description')
            form.save()
            messages.success(request, f'Successfully edited {a}')
            return redirect('view_module', pk, pk1)
    else:
        form = add_level_form(instance=a)
    return render(request, 'add_level.html', {"form": form})


def delete_level(request, pk):
    a = get_object_or_404(module_level, pk=pk)
    if request.method == "POST":
        q = module_level.objects.get(pk=pk)
        a1 = q.level_description
        messages.success(request, f'Successfully Deleted {a1}')
        q.delete()
        return redirect('home')

    return render(request, 'delete_level.html', {"a": a})


def view_module(request, pk, pk1):
    program1 = get_object_or_404(program, pk=pk)
    module1 = get_object_or_404(program_module, pk=pk1)
    questions1 = [q for q in question.objects.all() if q.module ==
                  module1 or q.level == None]
    # questions1 = question.objects.filter(module=module1, level_id=None)
    levels = module_level.objects.filter(module=module1)
    if len(levels) == 0:
        check = False
    else:
        check = True

    if len(questions1) == 0:
        check1 = False

    else:
        check1 = True

    paginator = Paginator(questions1, paginator_num_pages)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        questions11 = paginator.page(page)
    except:
        questions11 = paginator.page(paginator_num_pages)
    return render(request, 'view_module.html', {"p1": program1, "m": module1, "l": levels, "p": questions11, "check": check, 'check1': check1})


def view_facilitator(request, pk):
    facilitator1 = get_object_or_404(facilitator, pk=pk)
    return render(request, 'view_facilitator.html', {"f": facilitator1})


def view_level(request, pk, pk1, pk2):
    level1 = module_level.objects.get(pk=pk2)
    questions1 = question.objects.filter(level_id=level1)
    paginator = Paginator(questions1, paginator_num_pages)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        questions11 = paginator.page(page)
    except:
        questions11 = paginator.page(paginator_num_pages)
    return render(request, 'view_level.html', {"l": level1, "p": questions11})


def view_student(request, pk):
    student1 = get_object_or_404(student, pk=pk)
    return render(request, 'view_student.html', {"f": student1})


def view_batch(request, pk):
    batch1 = get_object_or_404(batch, pk=pk)
    return render(request, 'view_batch.html', {"f": batch1})


def view_center(request, pk):
    center1 = get_object_or_404(center, pk=pk)
    return render(request, 'view_center.html', {"f": center1})


def view_questions(request, pk):
    question1 = get_object_or_404(question, pk=pk)
    if question1.question_type.pk in [7, 8, 9]:
        question1.sub_questions = question.objects.filter(
            question_content=question1.question_content)

    template = f'view_question/sub_view/{question1.question_type.question_type_id}.html'
    try:
        django.template.loader.get_template(template)
    except:
        return HttpResponseNotFound("template not found")

    return render(request, template, {"f": question1})


def students(request):
    students = student.objects.all()
    paginator = Paginator(students, paginator_num_pages)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        students1 = paginator.page(page)
    except:
        students1 = paginator.page(paginator_num_pages)

    return render(request, 'students.html', {"p": students1})


def student_search(request):
    student_id = request.GET.get('student_id')
    stud = student.objects.all()
    stud1 = []
    for i in stud:
        if student_id in i.first_name:
            stud1.append(i)
        elif student_id in i.last_name:
            stud1.append(i)
    print(stud1)
    return render(request, 'ajax/student_search.html', {"m": stud1})


def centers(request):
    centers = center.objects.all()
    batches = batch.objects.all()
    for i in centers:
        for j in batches:
            if i == j.center_id:
                i.batch_check = True
    paginator = Paginator(centers, paginator_num_pages)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        centers1 = paginator.page(page)
    except:
        centers1 = paginator.page(paginator_num_pages)

    return render(request, 'centers.html', {"p": centers1})


def facilitators(request):
    facilitators = facilitator.objects.all()
    paginator = Paginator(facilitators, paginator_num_pages)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        fac1 = paginator.page(page)
    except:
        fac1 = paginator.page(paginator_num_pages)
    return render(request, 'facilitators.html', {"p": fac1})


def batches(request):
    batches = batch.objects.all()
    paginator = Paginator(batches, paginator_num_pages)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        batch1 = paginator.page(page)
    except:
        batch1 = paginator.page(paginator_num_pages)
    return render(request, 'batches.html', {"p": batch1})


def batch_search(request):
    batch_id = request.GET.get('batch_id')
    bat = batch.objects.all()
    bat1 = []
    for i in bat:
        if batch_id.lower() in i.batch_name:
            bat1.append(i)
    print(bat1)
    return render(request, 'ajax/batch_search.html', {"m": bat1})


def questionss(request):
    questions1 = question.objects.all()
    paginator = Paginator(questions1, paginator_num_pages)
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    try:
        questions11 = paginator.page(page)
    except:
        questions11 = paginator.page(paginator_num_pages)

    return render(request, 'questions.html', {"p": questions11})


@login_required
def add_question(request):
    if request.method == "POST":
        # manipulation to map incoming data to question form
        form = add_question_form(request.POST)
        option_formset = add_option_formset(request.POST)
        option_formset.data = option_formset.data.copy()
        form.data = form.data.copy()

        if request.POST['question_type'] in ['2', '4']:
            option_formset.data['form-0-is_right_option'] = True

        if request.POST['question_type'] == '5':
            if 'question_image' in request.FILES:
                form.instance.question_content = question_content(
                    content=request.FILES['question_image'])

        if request.POST['question_type'] == '6':
            option_formset.option_contents = {}
            for i in range(len(option_formset)):
                if f'form-{i}-option_description_file' in request.FILES:
                    option_content = question_content(
                        content=request.FILES[f'form-{i}-option_description_file'])
                    option_formset.option_contents[i] = option_content
                    option_formset.data[f'form-{i}-option_description'] = i

        if request.POST['question_type'] in ['7', '8', '9']:
            if request.POST['question_content_id'] != '':
                pk = int(request.POST['question_content_id'])
                if len(question_content.objects.filter(pk=pk)):
                    form.instance.question_content = question_content.objects.get(
                        pk=pk)
            elif 'question_content' in request.FILES:
                form.instance.question_content = question_content(
                    content=request.FILES['question_content'])

        # validation and sending back errors
        if not (form.is_valid() and option_formset.is_valid()):
            data = {'ok': False, 'message': ''}

            question_errors = form.errors.as_data()
            option_errors = str(option_formset.non_form_errors())

            if len(question_errors) > 0:
                error_field = str(list(question_errors.keys())[0])
                error = str(question_errors[error_field][0]).strip("[]'")
                error_field = error_field.replace('_', ' ')
                data['message'] = f'{error_field.capitalize()}: {error}'

            elif len(option_errors) > 0:
                data['message'] = option_errors

            return JsonResponse(data)

        # saving data if valid
        else:
            data = {'ok': True}

            if request.POST['question_type'] == '6':
                for i in range(len(option_formset)):
                    option_formset.option_contents[i].save()
                    option_formset[i].instance.option_description = str(
                        option_formset.option_contents[i])

            if request.POST['question_type'] in ['5', '7', '8', '9']:
                form.cleaned_data['question_content'].save()

            question = form.save()

            for option_form in option_formset:
                option_form.instance.question = question
                option_form.save()
            messages.success(request, f'Successfully Added Question')

            return JsonResponse(data)

    else:
        form = add_question_form()
        option_formset = add_option_formset()
        form.fields['question_type'].queryset = question_type.objects.exclude(
            Q(pk=1) | Q(pk=10) | Q(pk=11))
    return render(request, 'add_question/main.html', {"form": form, "option_formset": option_formset})


@login_required
def question_type_form(request):
    form_question_type = request.GET['question_type']

    template = f"add_question/sub_form/{form_question_type}.html"
    try:
        django.template.loader.get_template(template)
    except:
        return HttpResponse("")

    form_data = {}
    form_data["form"] = add_question_form()
    form_data["option_formset"] = add_option_formset()

    return render(request, template, form_data)


@login_required
def edit_question(request, pk):
    a = question.objects.get(pk=pk)
    form_question_type = a.question_type.pk

    if request.method == "POST":
        form = add_question_form(request.POST, request.FILES, instance=a)
        option_formset = add_option_formset(request.POST)
        option_formset.data = option_formset.data.copy()
        form.data = form.data.copy()
        # form.data['level'] = a.level.pk
        # form.data['module'] = a.module.pk
        # form.data['program'] = a.program.pk
        form.data['question_type'] = form_question_type

        if form_question_type in [2, 4]:
            option_formset.data['form-0-is_right_option'] = True

        if form_question_type == 5:
            if 'question_image' in request.FILES:
                form.instance.question_content = question_content(
                    content=request.FILES['question_image'])

        if form_question_type == 6:
            option_formset.option_contents = {}
            for i in range(len(option_formset)):
                if f'form-{i}-option_description_file' in request.FILES:
                    option_content = question_content(
                        content=request.FILES[f'form-{i}-option_description_file'])
                else:
                    option_content = question_content.objects.get(
                        content=str(a.options[i]))
                option_formset.option_contents[i] = option_content
                option_formset.data[f'form-{i}-option_description'] = i

        if form_question_type in [7, 8, 9]:
            sub_questions = question.objects.filter(
                question_content=a.question_content)
            if 'question_content' in request.FILES:
                form.instance.question_content = question_content(
                    content=request.FILES['question_content'])

        if not (form.is_valid() and option_formset.is_valid()):
            data = {'ok': False, 'message': ''}

            question_errors = form.errors.as_data()
            option_errors = str(option_formset.non_form_errors())

            if len(question_errors) > 0:
                error_field = str(list(question_errors.keys())[0])
                error = str(question_errors[error_field][0]).strip("[]'")
                error_field = error_field.replace('_', ' ')
                data['message'] = f'{error_field.capitalize()}: {error}'

            elif len(option_errors) > 0:
                data['message'] = option_errors

            return JsonResponse(data)
        else:
            data = {'ok': True}
            if form_question_type == 5:
                form.cleaned_data['question_content'].save()

            elif form_question_type == 6:
                for i in range(len(option_formset)):
                    option_formset.option_contents[i].save()
                    option_formset[i].instance.option_description = str(
                        option_formset.option_contents[i])

            elif form_question_type in [7, 8, 9]:
                form.cleaned_data['question_content'].save()
                for sub_question in sub_questions:
                    sub_question.level = form.cleaned_data['level']
                    sub_question.question_content = form.cleaned_data['question_content']
                    sub_question.save()

            form_question = form.save()

            for option in form_question.options:
                option.delete()

            for option_form in (option_formset):
                option_form.instance.question = form_question
                option_form.save()

            messages.success(request, f'Successfully Edited questions')
            return JsonResponse(data)
    else:
        template = f"edit_question/sub_form/{form_question_type}.html"
        form = add_question_form(instance=a)
        option_formset = add_option_formset(initial=a.options.values())
        return render(request, template, {"form": form, 'option_formset': option_formset})


def delete_question(request, pk):
    a = get_object_or_404(question, pk=pk)
    if request.method == "POST":
        q = question.objects.get(pk=pk)
        a1 = q.question_id
        messages.success(request, f'Successfully Deleted {a1}')
        q.delete()
        return redirect('questions')
    return render(request, 'delete_question.html', {"a": a})


def load_modules(request):
    program_id = request.GET.get('program_id')
    modules = program_module.objects.filter(program_id=program_id)
    return render(request, 'ajax/module_dropdown_list_options.html', {"m": modules})


def load_levels(request):
    module_id = request.GET.get('module_id')
    levels = module_level.objects.filter(module_id=module_id)
    return render(request, 'ajax/level_dropdown_list_options.html', {"m": levels})


@login_required
def add_facilitator(request):
    if request.method == "POST":
        form = add_facilitator_form(request.POST, request.FILES)
        if form.is_valid():
            a = form.cleaned_data.get('first_name')
            form.save()
            messages.success(request, f'Successfully Added {a}')
            return redirect('home')
    else:
        form = add_facilitator_form()

    return render(request, 'add_facilitator.html', {"form": form})


@login_required
def edit_facilitator(request, pk):
    a = facilitator.objects.get(pk=pk)
    if request.method == "POST":
        form = add_facilitator_form(request.POST, request.FILES, instance=a)
        if form.is_valid():
            a = form.cleaned_data.get('first_name')
            form.save()
            messages.success(request, f'Successfully Edited {a}')
            return redirect('facilitators')
    else:
        form = add_facilitator_form(instance=a)

    return render(request, 'add_facilitator.html', {"form": form, "f": a})


def delete_facilitator(request, pk):
    a = get_object_or_404(facilitator, pk=pk)
    if request.method == "POST":
        q = facilitator.objects.get(pk=pk)
        a1 = q.first_name
        messages.success(request, f'Successfully Deleted {a1}')
        q.delete()
        return redirect('home')

    return render(request, 'delete_facilitator.html', {"a": a})


@login_required
def add_student(request):
    if request.method == "POST":
        form = add_student_form(request.POST, request.FILES)
        if form.is_valid():
            a = form.cleaned_data.get('first_name')
            form.save()
            messages.success(request, f'Successfully Added{a}')
            return redirect('students')
    else:
        form = add_student_form()

    return render(request, 'add_student.html', {"form": form})


@login_required
def edit_student(request, pk):
    a = student.objects.get(pk=pk)
    if request.method == "POST":
        form = add_student_form(request.POST, request.FILES, instance=a)
        if form.is_valid():
            a = form.cleaned_data.get('first_name')
            form.save()
            messages.success(request, f'Successfully edited {a}')
            return redirect('students')
    else:
        form = add_student_form(instance=a)

    return render(request, 'add_student.html', {"form": form, "f": a})


def delete_student(request, pk):
    a = get_object_or_404(student, pk=pk)
    if request.method == "POST":
        q = student.objects.get(pk=pk)
        a1 = q.first_name
        messages.success(request, f'Successfully Deleted {a1}')
        q.delete()
        return redirect('students')

    return render(request, 'delete_student.html', {"a": a})


@login_required
def add_center(request):
    if request.method == "POST":
        form = add_center_form(request.POST)
        if form.is_valid():
            a = form.cleaned_data.get('center_name')
            form.save()
            messages.success(request, f'Successfully Added {a}')
            return redirect('centers')
    else:
        form = add_center_form()

    return render(request, 'add_center.html', {"form": form})


@login_required
def edit_center(request, pk):
    a = center.objects.get(pk=pk)
    if request.method == "POST":
        form = add_center_form(request.POST, instance=a)
        if form.is_valid():
            a = form.cleaned_data.get('center_name')
            form.save()
            messages.success(request, f'Successfully edited {a}')
            return redirect('centers')
    else:
        form = add_center_form(instance=a)

    return render(request, 'add_center.html', {"form": form})


def delete_center(request, pk):
    a = get_object_or_404(center, pk=pk)
    if request.method == "POST":
        q = center.objects.get(pk=pk)
        a1 = q.center_name
        messages.success(request, f'Successfully Deleted {a1}')
        q.delete()
        return redirect('centers')

    return render(request, 'delete_center.html', {"a": a})


@login_required
def add_batch(request):
    if request.method == "POST":
        form = add_batch_form(request.POST)
        if form.is_valid():
            form.end()
            a = form.cleaned_data.get('batch_name')
            form.save()
            messages.success(request, f'Successfully edited {a}')
            return redirect('batches')
    else:
        form = add_batch_form()

    return render(request, 'add_batch.html', {"form": form})


def edit_batch(request, pk):
    a = batch.objects.get(pk=pk)
    center_b = get_object_or_404(center, pk=a.center_id.center_id)
    if request.method == "POST":
        form = add_batch_form(request.POST, instance=a)
        if form.is_valid():
            # if not form.end():
            #     form.add_error('end_date', forms.ValidationError("The End_date cannot be before Start_Date"))
            #     return redirect('edit_batch',pk)
            a = form.cleaned_data.get('batch_name')
            form.save()
            messages.success(request, f'Successfully edited {a}')
            return redirect('batches')
    else:
        form = add_batch_form(instance=a)

    return render(request, 'add_batch.html', {"form": form, "f": a})


def delete_batch(request, pk):
    a = get_object_or_404(batch, pk=pk)
    if request.method == "POST":
        q = batch.objects.get(pk=pk)
        a1 = q.batch_name
        messages.success(request, f'Successfully Deleted {a1}')
        return redirect('batches')

    return render(request, 'delete_batch.html', {"a": a})


def password(request):
    return render(request, 'password.html')


def password_management_facilitators(request):
    facilitators = facilitator.objects.all()
    paginator = Paginator(facilitators, paginator_num_pages)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        facilitators1 = paginator.page(page)
    except:
        facilitators1 = paginator.page(paginator_num_pages)

    return render(request, 'password_management_facilitators.html', {"p": facilitators1})


def password_management_students(request):
    students = student.objects.all()
    paginator = Paginator(students, paginator_num_pages)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        students1 = paginator.page(page)
    except:
        students1 = paginator.page(paginator_num_pages)
    return render(request, 'password_management_students.html', {"p": students1})


def password_management_facilitator(request, pk):
    facilitator1 = facilitator.objects.get(pk=pk)
    if request.method == "POST":
        form = password_facilitator_form(
            request.POST, request.FILES, instance=facilitator1)
        if form.is_valid():
            a = facilitator1.first_name
            form.save()
            messages.success(request, f'Successfully changed password for {a}')
            return redirect('password_management_facilitators')
    else:
        form = password_facilitator_form()

    return render(request, 'password_management_facilitator.html', {"form": form, "f": facilitator1})


def password_management_student(request, pk):
    student1 = student.objects.get(pk=pk)
    if request.method == "POST":
        form = password_student_form(
            request.POST, request.FILES, instance=student1)
        if form.is_valid():
            a = student1.first_name
            form.save()
            messages.success(request, f'Successfully changed password for {a}')
            return redirect('password_management_students')
    else:
        form = password_student_form()

    return render(request, 'password_management_student.html', {"form": form, "s": student1})


class LoginView1(auth_views.LoginView):
    template_name = 'admin_login.html'
    form_class = AuthenticationForm


class LogoutView1(auth_views.LogoutView):
    template_name = 'admin_logout.html'
    form_class = AuthenticationForm
