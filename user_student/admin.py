from django.contrib import admin

from .models import scores,skillmaster,skills

#admin.site.register(student_status)
admin.site.register(scores)
admin.site.register(skills)
admin.site.register(skillmaster)
