from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user_admin.models import entity, entity_type, entity_status
from user_admin.models import student, facilitator, program, center
from user_admin.models import batch, program_module, module_level, question
from user_admin.models import student_module_level, student_batch,question_content,assessment_type
from mptt.models import MPTTModel, TreeForeignKey
#from user_admin.models import assessment_type
'''
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
'''



class scores(models.Model):
    student_id = models.ForeignKey(student, on_delete=models.CASCADE,null=False, blank=False)
    batch_id      = models.ForeignKey(batch, on_delete=models.CASCADE,null=False, blank=False)
    level_id      = models.ForeignKey(module_level, on_delete=models.CASCADE,null=False, blank=False)
    date_time     = models.TextField(null=False, blank=False)
    user_score    = models.IntegerField(null=False) # for particular test
    total_score   = models.IntegerField(null=False) # no.of tests taken
    question_content_id = models.IntegerField(null=True, blank=True)
    assessment_type_id = models.ForeignKey(assessment_type,on_delete=models.DO_NOTHING, null=True, blank=True)
    def __str__(self):
        return str(self.user_score)


class skillmaster(models.Model):
    skillid = models.IntegerField(primary_key=True)
    skillname = models.CharField(max_length=30)
    skilltype = models.CharField(max_length=20)
    skilldescription = models.TextField()

    def __str__(self):
        return self.skillname

    class Meta:
        verbose_name_plural = "Skillmaster"

class skills(models.Model):
    student_skill_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(student, on_delete=models.CASCADE, null=True)
    skillid = models.ForeignKey(skillmaster, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.student_id)

    class Meta:
        verbose_name_plural = "Skills"
        
        
class Course(models.Model):
    name = models.CharField(max_length=50, unique= True)
    def __str__(self):
        return self.name

class Stream(MPTTModel):
    name = models.CharField(max_length=50, unique=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name= 'course_name')
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return ("Stream {0} :: Course{1}".format(self.name, self.course_name))


class Job(models.Model):
    job_name = models.CharField(max_length=40)
    course = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True, related_name='couse_job')

    def __str__(self):
        return self.job_name

class Exam(models.Model):
    exam_name = models.CharField(max_length=40)
    def __str__(self):
        return self.exam_name

class Prereq_exam(models.Model):
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True, related_name='exam_main')
    course = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True, related_name='couse_exam')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, related_name='job_exam')
    
    
    def __str__(self):
        return ("{0} - {1} - {2}".format(self.exam, self.course, self.job))
