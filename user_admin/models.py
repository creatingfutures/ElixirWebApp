from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


def validate_not_spaces(value):
    if isinstance(value, str) and value.strip() == '':
        raise ValidationError(u"You must provide more than just whitespace.")


class entity(models.Model):
    class Meta:
        verbose_name_plural = "entities"
    entity_name = models.CharField(
        primary_key=True, max_length=100, unique=True)

    def __str__(self):
        return self.entity_name


def get_def():
    return entity.objects.get(entity_name="Facilitator")


class entity_status(models.Model):
    class Meta:
        verbose_name_plural = "entity_statuses"
    entity = models.ForeignKey(
        entity, on_delete=models.CASCADE, null=False, blank=False, default=get_def)
    status = models.IntegerField(primary_key=True)
    description = models.CharField(
        max_length=100, null=False, blank=False, validators=[validate_not_spaces])

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description = self.description.lower()
        return super(entity_type, self).save(*args, **kwargs)


class entity_type(models.Model):
    enitity = models.ForeignKey(entity, on_delete=models.CASCADE)
    entity_type_id = models.AutoField(primary_key=True)
    description = models.CharField(
        max_length=100, null=False, blank=False, unique=True, validators=[validate_not_spaces])

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description = self.description.lower()
        return super(entity_type, self).save(*args, **kwargs)


class student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(
        max_length=100, null=False, blank=False, validators=[validate_not_spaces])
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=True, blank=True)
    status = models.ForeignKey(entity_status, on_delete=models.CASCADE)
    landline_number = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, null=False, blank=False)
    email_id = models.CharField(max_length=100, null=False, blank=False)
    gender_choices = (
        ('M', 'M'), ('F', 'F')
    )
    gender = models.CharField(
        max_length=1, choices=gender_choices, null=False, blank=False)
    enroll_date = models.DateField(null=True, blank=True)
    dob = models.DateField(null=False, blank=False)
    address_1 = models.CharField(max_length=100, null=False, blank=False)
    school = models.CharField(max_length=100, null=True, blank=True)
    languages = models.CharField(max_length=100)
    comments = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(default="none.jpg", upload_to="student_images")

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        return super(student, self).save(*args, **kwargs)


class facilitator(models.Model):
    facilitator_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    dob = models.DateField(null=False, blank=False)
    occupation = models.CharField(max_length=100)
    specified_interests = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=True, blank=True)
    status = models.ForeignKey(entity_status, on_delete=models.CASCADE)
    landline_number = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, null=False, blank=False)
    email_id = models.CharField(max_length=100, null=False, blank=False)
    gender_choices = (
        ('M', 'M'), ('F', 'F')
    )
    gender = models.CharField(max_length=1, null=False,
                              blank=False, choices=gender_choices)
    enroll_date = models.DateField(null=True, blank=True)
    address_1 = models.CharField(max_length=100, null=False, blank=False)
    languages = models.CharField(max_length=100)
    comments = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(
        default="none.jpg", upload_to="facilitator_images")

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        return super(facilitator, self).save(*args, **kwargs)


class program(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_name = models.CharField(
        max_length=100, null=False, blank=False, unique=True)
    prerequisite = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.program_name

    def save(self, *args, **kwargs):
        self.program_name = self.program_name.lower()
        return super(program, self).save(*args, **kwargs)


class center(models.Model):
    center_id = models.AutoField(primary_key=True)
    center_name = models.CharField(
        max_length=100, null=False, blank=False, unique=True)
    address_1 = models.CharField(max_length=100, null=False, blank=False)
    comments = models.CharField(max_length=100, null=True, blank=True)
    landline_number = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, null=False, blank=False)
    email_id = models.CharField(max_length=100, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=False, blank=False)
    center_type = models.ForeignKey(entity_type, on_delete=models.CASCADE)
    batch_check = models.BooleanField(default=False)

    def __str__(self):
        return self.center_name

    def save(self, *args, **kwargs):
        self.center_name = self.center_name.lower()
        return super(center, self).save(*args, **kwargs)


class batch(models.Model):
    class Meta:
        verbose_name_plural = "batches"
    batch_id = models.AutoField(primary_key=True)
    program_id = models.ForeignKey(program, on_delete=models.CASCADE)
    batch_name = models.CharField(
        max_length=100, null=True, blank=True, unique=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(entity_status, on_delete=models.CASCADE)
    batch_incharge_id = models.ForeignKey(
        facilitator, on_delete=models.CASCADE)
    partner_org = models.CharField(max_length=100, null=True, blank=True)
    center_id = models.ForeignKey(center, on_delete=models.CASCADE)
    sessions_count = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)])
    student_count = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)])
    comments = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.batch_name

    def save(self, *args, **kwargs):
        self.batch_name = self.batch_name.lower()
        return super(batch, self).save(*args, **kwargs)


class program_module(models.Model):
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=100, null=False, blank=False)
    program = models.ForeignKey(program, on_delete=models.CASCADE)
    comments = models.CharField(max_length=500, null=True, blank=False)

    def __str__(self):
        return self.module_name

    def save(self, *args, **kwargs):
        self.module_name = self.module_name.lower()
        return super(program_module, self).save(*args, **kwargs)


class module_level(models.Model):
    level_id = models.AutoField(primary_key=True)
    module = models.ForeignKey(program_module, on_delete=models.CASCADE)
    level_description = models.CharField(
        max_length=100, null=False, blank=False)

    def __str__(self):
        return self.level_description

    def save(self, *args, **kwargs):
        self.level_description = self.level_description.lower()
        return super(module_level, self).save(*args, **kwargs)


class question_type(models.Model):
    question_type_id = models.AutoField(primary_key=True)
    question_type = models.CharField(
        max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.question_type.capitalize()

    def save(self, *args, **kwargs):
        self.question_type = self.question_type.lower()
        return super(question_type, self).save(*args, **kwargs)


class question_content(models.Model):
    question_content_id = models.AutoField(primary_key=True)
    content = models.FileField(upload_to='question_content')

    def __str__(self):
        return str(self.content)


class question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_type = models.ForeignKey(
        question_type, on_delete=models.CASCADE, blank=False, null=False)
    level = models.ForeignKey(
        module_level, on_delete=models.CASCADE, null=False, blank=False)
    question = models.CharField(
        max_length=200, null=False, blank=False)
    narrative = models.CharField(max_length=100, null=True, blank=True)
    hint = models.CharField(max_length=100, null=True, blank=True)
    comments = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    question_content = models.ForeignKey(
        question_content, on_delete=models.DO_NOTHING, null=True, blank=True)

    @property
    def program(self):
        return self.module.program

    @property
    def module(self):
        return self.level.module

    @property
    def options(self):
        return question_option.objects.filter(question=self)

    @property
    def answer(self):
        try:
            return question_option.objects.get(question=self, is_right_option=True)
        except:
            return "No Answer"
    @property
    def content(self):
        return question_content.objects.get(question=self)

    def __str__(self):
        return self.question


class question_option(models.Model):
    question = models.ForeignKey(
        question, on_delete=models.CASCADE, null=False, blank=False)
    option_description = models.CharField(
        max_length=200, null=False, blank=False)
    is_right_option = models.BooleanField(
        blank=False, null=False)

    def __str__(self):
        return self.option_description


class student_module_level(models.Model):
    student_student_id = models.ForeignKey(student, on_delete=models.CASCADE)
    module_level_id = models.ForeignKey(module_level, on_delete=models.CASCADE)


class student_batch(models.Model):
    class Meta:
        verbose_name_plural = "student_batches"
    student_id = models.ForeignKey(student, on_delete=models.CASCADE)
    batch_id = models.ForeignKey(batch, on_delete=models.CASCADE)
    program_id = models.ForeignKey(program, on_delete=models.CASCADE)
