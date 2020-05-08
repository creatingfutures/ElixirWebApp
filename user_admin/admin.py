from django.contrib import admin

from .models import entity,entity_type,entity_status
from .models import student,facilitator,program,center
from .models import batch,program_module,module_level,questions
from .models import student_module_level,student_batch

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
admin.site.register(questions)
admin.site.register(student_module_level)
admin.site.register(student_batch)
