from django.contrib import admin

from .models import entity,entity_type,entity_status
from .models import student,facilitator,program,center

admin.site.register(entity)
admin.site.register(entity_type)
admin.site.register(entity_status)
admin.site.register(student)
admin.site.register(facilitator)
admin.site.register(program)
admin.site.register(center)
