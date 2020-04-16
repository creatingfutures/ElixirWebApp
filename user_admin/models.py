from django.db import models


class entity(models.Model):
    entity_name = models.CharField(primary_key=True,max_length=100,unique=True)

class entity_status(models.Model):
    status = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100,null=False,blank=False,unique=True)
    def __str__(self):
        return self.description

class entity_type(models.Model):
    enitity=models.ForeignKey(entity,on_delete=models.CASCADE)
    entity_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100,null=False,blank=False,unique=True)
    def __str__(self):
        return self.description



class student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name =  models.CharField(max_length=100,null=True,blank=True)
    last_name =  models.CharField(max_length=100,null=False,blank=False)
    password =  models.CharField(default="creatingfuturesS",max_length=100,null=False,blank=False)
    status = models.ForeignKey(entity_status,on_delete=models.CASCADE)
    landline_number =  models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=100,null=False,blank=False)
    email_id = models.CharField(max_length=100,null=False,blank=False)
    gender = models.CharField(max_length=1,null=False,blank=False)
    enroll_date =  models.DateField(null=True, blank=True)
    dob = models.DateField(null=False,blank=False)
    address_1 = models.CharField(max_length=100,null=False,blank=False)
    address_2 = models.CharField(max_length=100,null=False,blank=False)
    school = models.CharField(max_length=100,null=True,blank=True)
    languages = models.CharField(max_length=100)
    comments = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(default="none.jpg",upload_to="student_images")
    def __str__(self):
        return self.first_name

    def save(self,*args,**kwargs):
        self.first_name=self.first_name.lower()
        self.last_name=self.last_name.lower()
        return super(student,self).save(*args,**kwargs)

class facilitator(models.Model):
    facilitator_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name =  models.CharField(max_length=100,null=True,blank=True)
    last_name =  models.CharField(max_length=100,null=False,blank=False)
    dob = models.DateField(null=False,blank=False)
    occupation = models.CharField(max_length=100)
    specified_interests = models.CharField(max_length=100)
    password =  models.CharField(max_length=100,default="creatingfuturesF",null=False,blank=False)
    status = models.ForeignKey(entity_status,on_delete=models.CASCADE)
    landline_number =  models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=100,null=False,blank=False)
    email_id = models.CharField(max_length=100,null=False,blank=False)
    gender = models.CharField(max_length=1,null=False,blank=False)
    enroll_date =  models.DateField(null=True, blank=True)
    address_1 = models.CharField(max_length=100,null=False,blank=False)
    address_2 = models.CharField(max_length=100,null=False,blank=False)
    languages = models.CharField(max_length=100)
    comments = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(default="none.jpg",upload_to="facilitator_images")
    def __str__(self):
        return self.first_name
    def save(self,*args,**kwargs):
        self.first_name=self.first_name.lower()
        self.last_name=self.last_name.lower()
        return super(facilitator,self).save(*args,**kwargs)

class program(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=100,null=False,blank=False,unique=True)
    prerequisite =  models.CharField(max_length=100,null=True,blank=True)
    comments = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.program_name

class center(models.Model):
    center_id = models.AutoField(primary_key=True)
    center_name = models.CharField(max_length=100,null=False,blank=False,unique=True)
    address_1 = models.CharField(max_length=100,null=False,blank=False)
    address_2 = models.CharField(max_length=100,null=False,blank=False)
    comments = models.CharField(max_length=100,null=True,blank=True)
    landline_number =  models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=100,null=False,blank=False)
    email_id = models.CharField(max_length=100,null=False,blank=False)
    contact_person = models.CharField(max_length=100,null=False,blank=False)
    center_type = models.ForeignKey(entity_type,on_delete=models.CASCADE)
    def __str__(self):
        return self.center_name

class batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    program_id = models.ForeignKey(program,on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=100,null=True,blank=True,unique=True)
    start_date  = models.DateField(null=False,blank=False)
    end_date = models.DateField(null=False,blank=False)
    status = models.ForeignKey(entity_status,on_delete=models.CASCADE)
    batch_incharge_id = models.ForeignKey(facilitator,on_delete=models.CASCADE)
    partner_org = models.CharField(max_length=100,null=True,blank=True)
    center_id = models.ForeignKey(center,on_delete=models.CASCADE)
    sessions_count = models.IntegerField(null=True,blank=True)
    student_count = models.IntegerField(null=True,blank=True)
    comments = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.batch_name
    def save(self,*args,**kwargs):
        self.batch_name=self.batch_name.lower()
        return super(batch,self).save(*args,**kwargs)

class program_module(models.Model):
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=100,null=False,blank=False,unique=True)
    program_id = models.ForeignKey(program,on_delete=models.CASCADE)
    def __str__(self):
        return self.module_name


class module_level(models.Model):
    level_id = models.AutoField(primary_key=True)
    module_id = models.ForeignKey(program_module,on_delete=models.CASCADE)
    level_number = models.IntegerField(null=False,blank=False,unique=True)
    level_description = models.CharField(max_length=100,null=True,blank=True,unique=True)
    def __str__(self):
        return self.level_description

class questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=100,null=True,blank=True,unique=True)
    answer = models.CharField(max_length=500,null=True,blank=True)
    level_id = models.ForeignKey(module_level,on_delete=models.CASCADE,null=True,blank=True)
    program_id = models.ForeignKey(program,on_delete=models.CASCADE,null=False,blank=False)
    module_id = models.ForeignKey(program_module,on_delete=models.CASCADE,null=True,blank=True)
    question_type = models.CharField(max_length=100,null=True,blank=True)
    narrative = models.CharField(max_length=100,null=True,blank=True)
    option1 = models.CharField(max_length=100,null=True,blank=True)
    option2 = models.CharField(max_length=100,null=True,blank=True)
    option3 = models.CharField(max_length=100,null=True,blank=True)
    option4 = models.CharField(max_length=100,null=True,blank=True)
    comments = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.question

class student_module_level(models.Model):
    student_student_id = models.ForeignKey(student,on_delete=models.CASCADE)
    module_level_id = models.ForeignKey(module_level, on_delete=models.CASCADE)

class student_batch(models.Model):
    student_id = models.ForeignKey(student,on_delete=models.CASCADE)
    batch_id = models.ForeignKey(batch,on_delete=models.CASCADE)
    program_id = models.ForeignKey(program,on_delete=models.CASCADE)
