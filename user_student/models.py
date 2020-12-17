from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user_admin.models import entity, entity_type, entity_status
from user_admin.models import student, facilitator, program, center
from user_admin.models import batch, program_module, module_level, question
from user_admin.models import student_module_level, student_batch,question_content


class student_status(models.Model):
    class Meta:
        verbose_name_plural = "student_statuses"
    student_id = models.ForeignKey(student, on_delete=models.CASCADE)
    program_id = models.ForeignKey(program, on_delete=models.CASCADE)
    module_id = models.ForeignKey(program_module, on_delete=models.CASCADE)
    level_id = models.ForeignKey(module_level, on_delete=models.CASCADE)
    batch_id = models.ForeignKey(batch, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    score = models.IntegerField(validators=[MinValueValidator(0)]) # total score of all exams
    type_choices = (
        ('S_Pass', 'S_Pass'),
        ('S_Fail', 'S_Fail'),
        ('I_Pass', 'I_Pass'),
        ('I_Fail', 'I_Fail'),
        ('AV_Pass', 'AV_Pass'),
        ('AV_Fail', 'AV_Fail'),
        ('C_Pass', 'C_Pass'),
        ('C_Fail', 'C_Fail')
    )
    status = models.CharField(max_length=100, choices=type_choices)

    def __str__(self):
        return ''+self.student_id.first_name+'__'+self.program_id.program_name+'__'+self.module_id.module_name+'__'+self.level_id.level_description


class scores(models.Model):
    user_score    = models.IntegerField(null=False) # for particular test 
    student_id = models.ForeignKey(student, on_delete=models.CASCADE,null=True, blank=True) 
    batch_id      = models.ForeignKey(batch, on_delete=models.CASCADE,null=True, blank=True)
    level_id      = models.ForeignKey(module_level, on_delete=models.CASCADE,null=True, blank=True)
    date_time     = models.DateTimeField(null=True, blank=True)
    total_score   = models.IntegerField(default=0) # no.of tests taken 
    question_content_id = models.ForeignKey(question_content, on_delete=models.DO_NOTHING, null=True, blank=True)
    assesment_type = models.CharField(default="Narrative",max_length=20)        
    def __str__(self):
        return str(self.user_score)