from django.contrib import admin

from .models import student_status,scores

admin.site.register(student_status)
admin.site.register(scores)