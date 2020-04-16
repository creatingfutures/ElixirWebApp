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
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',auth_views.LoginView.as_view(template_name='admin_login.html'),name='admin_login'),
    path('home/',views.home,name='home'),
    path('add_program/',views.add_program,name='add_program'),
    path('view_program/<int:pk>/add_module',views.add_module,name='add_module'),
    path('view_program/<int:pk>/add_module/<int:pk1>/add_level',views.add_level,name='add_level'),

    path('add_facilitator/',views.add_facilitator,name='add_facilitator'),
    path('add_center/',views.add_center,name='add_center'),
    path('add_student/',views.add_student,name='add_student'),
    path('add_program/',views.add_program,name='add_program'),
    path('add_batch/',views.add_batch,name='add_batch'),
    path('add_question/',views.add_question,name='add_question'),

    path('ajax/load_modules/',views.load_modules,name='load_modules'),
    path('ajax/load_levels/',views.load_levels,name='load_levels'),

    path('ajax/load_modules_home/',views.load_modules_home,name='load_modules_home'),
    path('ajax/load_fac_home/',views.load_fac_home,name='load_fac_home'),
    path('ajax/student_search/',views.student_search,name='student_search'),
    path('ajax/batch_search/',views.batch_search,name='batch_search'),



    path('delete_program/<int:pk>',views.delete_program,name='delete_program'),
    path('delete_module/<int:pk>',views.delete_module,name='delete_module'),
    path('delete_level/<int:pk>',views.delete_level,name='delete_level'),
    path('delete_facilitator/<int:pk>',views.delete_facilitator,name='delete_facilitator'),
    path('delete_student/<int:pk>',views.delete_student,name='delete_student'),
    path('delete_center/<int:pk>',views.delete_center,name='delete_center'),
    path('delete_batch/<int:pk>',views.delete_batch,name='delete_batch'),
    path('delete_question/<int:pk>',views.delete_question,name='delete_question'),


    path('password/',views.password,name='password'),
    path('centers/',views.centers,name='centers'),
    path('students/',views.students,name='students'),
    path('facilitators/',views.facilitators,name='facilitators'),
    path('batches/',views.batches,name='batches'),
    path('questions/',views.questionss,name='questions'),



    path('view_program/<int:pk>/view_module/<int:pk1>',views.view_module,name='view_module'),
    path('view_facilitator/<int:pk>',views.view_facilitator,name='view_facilitator'),
    path('view_program/<int:pk>/edit_module/<int:pk1>/view_level/<int:pk2>',views.view_level,name='view_level'),



    path('edit_batch/<int:pk>',views.edit_batch,name='edit_batch'),
    path('edit_question/<int:pk>',views.edit_question,name='edit_question'),
    path('edit_facilitator/<int:pk>',views.edit_facilitator,name='edit_facilitator'),
    path('edit_center/<int:pk>',views.edit_center,name='edit_center'),
    path('edit_student/<int:pk>',views.edit_student,name='edit_student'),
    path('edit_program/<int:pk>',views.edit_program,name='edit_program'),
    path('view_program/<int:pk>/edit_module/<int:pk1>',views.edit_module,name='edit_module'),
    path('view_program/<int:pk>/edit_module/<int:pk1>/edit_level/<int:pk2>',views.edit_level,name='edit_level'),




    path('password_management_facilitators',views.password_management_facilitators,name='password_management_facilitators'),
    path('password_management_facilitator/<int:pk>',views.password_management_facilitator,name='password_management_facilitator'),
    path('password_management_students',views.password_management_students,name='password_management_students'),
    path('password_management_student/<int:pk>',views.password_management_student,name='password_management_student'),

    path('',views.LoginView1.as_view(),name='admin_login'),
    path('logout/',views.LogoutView1.as_view(),name='admin_logout'),


]
