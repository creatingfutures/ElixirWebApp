from django.contrib import admin

from .models import entity, entity_type, entity_status
from .models import student, facilitator, program, center
from .models import batch, program_module, module_level
from .models import student_module_level, student_batch
from .models import question, question_type, question_option, question_content
from .models import assessment_type
# from .models import image_question,images_question,av_question,av_sub_question

admin.site.register(entity)
admin.site.register(entity_type)
admin.site.register(entity_status)
admin.site.register(student)
admin.site.register(facilitator)
admin.site.register(program)
admin.site.register(center)

admin.site.register(batch)
admin.site.register(program_module)
admin.site.register(module_level)
admin.site.register(question)
admin.site.register(question_type)
admin.site.register(question_option)
admin.site.register(question_content)
admin.site.register(student_module_level)
admin.site.register(student_batch)


admin.site.register(assessment_type)
#admin.site.register(image_question)
# admin.site.register(images_question)
# admin.site.register(av_question)
# admin.site.register(av_sub_question)
