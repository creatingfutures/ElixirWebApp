from django.contrib import admin

from .models import scores,skillmaster,skills, Stream, Job, Exam, Course, Prereq_exam

#admin.site.register(student_status)
admin.site.register(scores)
admin.site.register(skills)
admin.site.register(skillmaster)
admin.site.register(Stream)
admin.site.register(Job)
admin.site.register(Exam)
admin.site.register(Prereq_exam)
admin.site.register(Course)
