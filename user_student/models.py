from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

from user_admin.models import entity,entity_type,entity_status
from user_admin.models import student,facilitator,program,center
from user_admin.models import batch,program_module,module_level,questions
from user_admin.models import student_module_level,student_batch

class student_status(models.Model):
    student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    program_id=models.ForeignKey(program,on_delete=models.CASCADE)
    module_id=models.ForeignKey(program_module,on_delete=models.CASCADE)
    level_id=models.ForeignKey(module_level,on_delete=models.CASCADE)
    batch_id=models.ForeignKey(batch,on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    score=models.IntegerField(validators=[MinValueValidator(0)])
    type_choices = (
    ('Pass', 'Pass'),
    ('Fail','Fail')
)
    status=models.CharField(max_length=100,choices=type_choices)
    def __str__(self):
        return ''+self.student_id.first_name+'__'+self.program_id.program_name+'__'+self.module_id.module_name+'__'+self.level_id.level_description
