from django.contrib import admin

from .models import scores,skillmaster,skills, Stream, Job, Exam, Course, Prereq_exam

#admin.site.register(student_status)
admin.site.register(skills)
admin.site.register(skillmaster)
admin.site.register(Stream)
admin.site.register(Job)
admin.site.register(Exam)
admin.site.register(Prereq_exam)
admin.site.register(Course)
@admin.register(scores)
class MemberAdmin(ImportExportModelAdmin):
    list_display = ('id','student_id','batch_id','level_id','date_time','user_score','total_score','question_content_id','assessment_type_id','updated_date')
    pass
