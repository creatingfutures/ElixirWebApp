
"""creating_futures URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_admin import views
from user_student import views as s_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',auth_views.LoginView.as_view(template_name='admin_login.html'),name='admin_login'),
    path('home/', views.home, name='home'),
    path('add_program/', views.add_program, name='add_program'),
    path('view_program/<int:pk>/add_module',
         views.add_module, name='add_module'),
    path('view_program/<int:pk>/add_module/<int:pk1>/add_level',
         views.add_level, name='add_level'),

    path('student_export', views.student_export, name='student_export'),
    path('questions_export', views.questions_export, name='questions_export'),
    path('view_student/<int:pk>', views.view_student, name='view_student'),
    path('view_batch/<int:pk>', views.view_batch, name='view_batch'),
    path('view_center/<int:pk>', views.view_center, name='view_center'),
    path('view_questions/<int:pk>', views.view_questions, name='view_questions'),

    path('add_facilitator/', views.add_facilitator, name='add_facilitator'),
    path('add_center/', views.add_center, name='add_center'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_program/', views.add_program, name='add_program'),
    path('add_batch/', views.add_batch, name='add_batch'),
    path('add_question/', views.add_question, name='add_question'),
    path('questions_import', views.questions_import, name='questions_import'), 
    path('ajax/load_modules/', views.load_modules, name='load_modules'),
    path('ajax/load_levels/', views.load_levels, name='load_levels'),
    path('ajax/load_modules_home/',
         views.load_modules_home, name='load_modules_home'),
    path('ajax/load_fac_home/', views.load_fac_home, name='load_fac_home'),
    path('ajax/student_search/', views.student_search, name='student_search'),
    path('ajax/batch_search/', views.batch_search, name='batch_search'),
    path('questions/ajax/questions_search', views.questions_search, name='questions_search'),
    path('ajax/pagination_search', views.questions_search, name='pagination_search'),
    path('ajax/question_type_form/',views.question_type_form, name='question_type_form'),
    path('delete_program/<int:pk>', views.delete_program, name='delete_program'),
    path('delete_module/<int:pk>', views.delete_module, name='delete_module'),
    path('delete_level/<int:pk>', views.delete_level, name='delete_level'),
    path('delete_facilitator/<int:pk>',views.delete_facilitator, name='delete_facilitator'),
    path('delete_student/<int:pk>', views.delete_student, name='delete_student'),
    path('delete_center/<int:pk>', views.delete_center, name='delete_center'),
    path('delete_batch/<int:pk>', views.delete_batch, name='delete_batch'),
    path('delete_question/<int:pk>', views.delete_question, name='delete_question'),

    path('password/', views.password, name='password'),
    path('centers/', views.centers, name='centers'),
    path('students/', views.students, name='students'),
    path('facilitators/', views.facilitators, name='facilitators'),
    path('batches/', views.batches, name='batches'),
    path('questions/', views.questionss, name='questions'),



    path('view_program/<int:pk>/view_module/<int:pk1>',
         views.view_module, name='view_module'),
    path('view_facilitator/<int:pk>',
         views.view_facilitator, name='view_facilitator'),
    path('view_program/<int:pk>/edit_module/<int:pk1>/view_level/<int:pk2>',
         views.view_level, name='view_level'),



    path('edit_batch/<int:pk>', views.edit_batch, name='edit_batch'),
    path('edit_question/<int:pk>', views.edit_question, name='edit_question'),
    path('edit_facilitator/<int:pk>',
         views.edit_facilitator, name='edit_facilitator'),
    path('edit_center/<int:pk>', views.edit_center, name='edit_center'),
    path('edit_student/<int:pk>', views.edit_student, name='edit_student'),
    path('edit_program/<int:pk>', views.edit_program, name='edit_program'),
    path('view_program/<int:pk>/edit_module/<int:pk1>',
         views.edit_module, name='edit_module'),
    path('view_program/<int:pk>/edit_module/<int:pk1>/edit_level/<int:pk2>',
         views.edit_level, name='edit_level'),




    path('password_management_facilitators', views.password_management_facilitators,
         name='password_management_facilitators'),
    path('password_management_facilitator/<int:pk>',
         views.password_management_facilitator, name='password_management_facilitator'),
    path('password_management_students', views.password_management_students,
         name='password_management_students'),
    path('password_management_student/<int:pk>', 
         views.password_management_student, name='password_management_student'),
    path('admin_login', views.LoginView1.as_view(), name='admin_login'),
    path('logout/', views.LogoutView1.as_view(), name='admin_logout'),


    path('', s_views.login, name='student_login'),
    path('s_home/<int:pk>/batch/<int:pk1>', s_views.s_home, name="s_home"),

    path('s_home/<int:pk>/batch/<int:pk1>/program/<str:programName>',
         s_views.spoken_english, name="spoken_english"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:m>/level/<int:l>/crossword/<str:narrative>/<int:assessment_type_id>', s_views.crossword, name="crossword"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:m>/level/<int:l>/word_find/<str:narrative>/<int:assessment_type_id>', s_views.word_find, name="word_find"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:m>/level/<int:l>/list_narrative/match/<str:narrative>/<int:assessment_type_id>', s_views.match, name="match"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:m>/level/<int:l>/list_narrative/<int:assessment_type_id>', s_views.list_narrative, name="list_narrative"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/lesson',s_views.lesson,name="lesson"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:m>/level/<int:l>/score_save/<int:typ>/<int:score>/<int:total_score>', s_views.score_save, name="score_save"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/',
         s_views.module_view, name="module_view"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>',
         s_views.level_view, name="level_view"),
#     path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/lesson/',
#          s_views.lesson, name="lesson"),

    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/btest/',
         s_views.before_test, name="before_test"),

#   path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/crossword/',
#          s_views.crossword, name="crossword"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/resume_builder/',
         s_views.resumebuilder, name="resumebuilder"),



    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/standard_test/',
         s_views.standard_test, name="standard_test"),

    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/standard_test/ajax/test/',
         s_views.ajax_standard_test, name='ajax_standard_test'),

    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/image_test/',
         s_views.image_test, name="image_test"),

    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/image_test/ajax/test/',
         s_views.ajax_image_test, name='ajax_image_test'),

    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/type/<int:pk5>/av_test/<str:narrative>',
         s_views.av_test, name="av_test"),

    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/type/<int:pk5>/av_test/ajax/test/<str:narrative>',
         s_views.ajax_av_test, name='ajax_av_test'),

    path('s_home/<int:pk>/batch/<int:pk1>/program/<int:pk2>/module/<int:pk3>/level/<int:pk4>/test/submit/',
         s_views.test_submit, name="test_submit"),


    path('error/', views.error, name="error"),


    path('facilitator_login/<int:pk>/<int:pk1>/<int:pk2>/<int:pk3>/<int:pk4>',s_views.facilitator_login,name='facilitator_login'),

    path('writing_scores/<int:pk>/<int:pk1>/<int:pk2>/<int:pk3>/<int:pk4>',s_views.writing_scores,name='writing_scores'),

    path('writing_test_submit/<int:pk>/<int:pk1>/<int:pk2>/<int:pk3>/<int:pk4>/<str:programName>',s_views.writing_test_submit,name='writing_test_submit'),
    
    path('s_home/<int:pk>/batch/<int:pk1>/program/<str:program>/Mi/', s_views.Mi_Test, name="Mi"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<str:program>/MyStrengths/', s_views.My_Strengths, name="MyStrengths"),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<str:program>/MIResult/', s_views.Mi_TestResult, name="MIResult" ),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<str:program>/LT/', s_views.Listen, name="LT" ),
    path('s_home/<int:pk>/batch/<int:pk1>/program/<str:program>/Lscore/', s_views.LScore, name="Lscore" ),
    #path('LHome/', s_views.LHome, name="LHome" ),
     #path('Mview/', s_views.Module_view_SK, name="Mview" ),
     #path('Mview1/', s_views.Module_view_LS, name="Mview1" ),
    # path('Mhome/', s_views.Mhome, name="Mhome" ),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL2, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL4, document_root=settings.MEDIA_ROOT)
