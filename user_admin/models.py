from django.db import models


class entity(models.Model):
    entity_name = models.CharField(primary_key=True,max_length=100)

class entity_status(models.Model):
    enitity=models.ForeignKey(entity,on_delete=models.CASCADE)
    status = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100,null=False,blank=False)

class entity_type(models.Model):
    enitity=models.ForeignKey(entity,on_delete=models.CASCADE)
    entity_type_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100,null=False,blank=False)


class student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name =  models.CharField(max_length=100,null=True,blank=True)
    last_name =  models.CharField(max_length=100,null=False,blank=False)
    status = models.ForeignKey(entity_status,on_delete=models.CASCADE)
    landline_number =  models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=100,null=False,blank=False)
    email_id = models.CharField(max_length=100,null=False,blank=False)
    gender = models.CharField(max_length=1,null=False,blank=False)
    enroll_date =  models.DateField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    addeess_1 = models.CharField(max_length=100,null=False,blank=False)
    address_2 = models.CharField(max_length=100,null=False,blank=False)
    school = models.CharField(max_length=100,null=True,blank=True)
    languages = models.CharField(max_length=100)
    comments = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(default="none.jpg",upload_to="student_images")

class facilitator(models.Model):
    facilitator_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name =  models.CharField(max_length=100,null=True,blank=True)
    last_name =  models.CharField(max_length=100,null=False,blank=False)
    dob = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=100)
    specified_interests = models.CharField(max_length=100)

    status = models.ForeignKey(entity_status,on_delete=models.CASCADE)
    landline_number =  models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=100,null=False,blank=False)
    email_id = models.CharField(max_length=100,null=False,blank=False)
    gender = models.CharField(max_length=1,null=False,blank=False)
    enroll_date =  models.DateField(null=True, blank=True)
    addeess_1 = models.CharField(max_length=100,null=False,blank=False)
    address_2 = models.CharField(max_length=100,null=False,blank=False)
    languages = models.CharField(max_length=100)
    comments = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(default="none.jpg",upload_to="facilitator_images")

class program(models.Model):
    program_id = models.IntegerField(primary_key=True)
    program_name = models.CharField(max_length=100,null=False,blank=False)
    prerequisite =  models.CharField(max_length=100,null=True,blank=True)
    comments = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100,null=True,blank=True)
    updated_by = models.CharField(max_length=100,null=True,blank=True)

class center(models.Model):
    center_id = models.IntegerField(primary_key=True)
    center_name = models.CharField(max_length=100,null=False,blank=False)
    addeess_1 = models.CharField(max_length=100,null=False,blank=False)
    address_2 = models.CharField(max_length=100,null=False,blank=False)
    comments = models.CharField(max_length=100,null=True,blank=True)
    landline_number =  models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=100,null=False,blank=False)
    email_id = models.CharField(max_length=100,null=False,blank=False)
    contact_person = models.CharField(max_length=100,null=False,blank=False)
    center_type = models.ForeignKey(entity_status,on_delete=models.CASCADE)
