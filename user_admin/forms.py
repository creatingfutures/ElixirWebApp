from django import forms

from .models import program, program_module, facilitator, center
from .models import student, module_level, question, batch, entity, entity_status, question_option, question_type
# from .models import image_question,images_question,av_question,av_sub_question
import datetime
import re


class add_program_form(forms.ModelForm):
    class Meta:
        model = program
        fields = ['program_name', 'prerequisite', 'comments']
        widgets = {'comments': forms.Textarea}


class add_module_form(forms.ModelForm):
    class Meta:
        model = program_module
        fields = ['module_name', 'comments']
        widgets = {'comments': forms.Textarea}

    def clean_module_name(self):
        m = self.instance.program_id
        l = self.cleaned_data['module_name']
        ls = program_module.objects.filter(program=m)
        for i in ls:
            if i == self.instance:
                continue
            if l == i.module_name:
                raise forms.ValidationError(
                    "A module with that name already exists for this program")
        return l


class add_level_form(forms.ModelForm):
    class Meta:
        model = module_level
        fields = ['level_description']

    def clean_level_description(self):
        m = self.instance.module_id
        l = self.cleaned_data['level_description']
        ls = module_level.objects.filter(module=m)
        for i in ls:
            if i == self.instance:
                continue
            if l == i.level_description:
                raise forms.ValidationError(
                    "A level with that description already exists for this module")
        return l


class add_question_form(forms.ModelForm):
    program = forms.ModelChoiceField(queryset=program.objects.all())
    module = forms.ModelChoiceField(queryset=program_module.objects.all())

    class Meta:
        model = question
        fields = ['question_type', 'level', 'question', 'narrative', 'hint', 'comments',
                  'created_by', 'updated_by', 'assessment_type', 'question_content']
        widgets = {'comments': forms.Textarea,
                   'question': forms.Textarea}

    def clean_question_content(self):
        question_type = self.cleaned_data["question_type"]
        if question_type.pk in [5, 7, 8, 9]:
            if not self.instance.question_content:
                raise forms.ValidationError('This field is required')
            else:
                return self.instance.question_content

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['module'].queryset = program_module.objects.none()
        self.fields['level'].queryset = module_level.objects.none()

        if 'program' in self.data:
            try:
                program = int(self.data.get('program'))
                self.fields['module'].queryset = program_module.objects.filter(
                    program=program)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['module'].queryset = self.instance.program.program_module_set
            self.fields['program'].initial = self.instance.program

        if 'module' in self.data:
            try:
                module = int(self.data.get('module'))
                self.fields['level'].queryset = module_level.objects.filter(
                    module=module)

            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['level'].queryset = self.instance.module.module_level_set
            self.fields['module'].initial = self.instance.module


class add_option_base_formset(forms.BaseFormSet):
    def clean(self):
        for form in self.forms:
            if form.instance.option_description == '':
                raise forms.ValidationError(
                    "Blank options not allowed")

        right_option_counter = 0
        for form in self.forms:
            if form.instance.is_right_option:
                right_option_counter += 1
        if right_option_counter != 1:
            raise forms.ValidationError(
                "Exactly one option should be correct")


add_option_formset = forms.modelformset_factory(model=question_option,
                                                fields=[
                                                    'option_description', 'is_right_option'],
                                                labels={
                                                    'option_description': 'Option ', 'is_right_option': 'Answer'},
                                                max_num=4,
                                                extra=1,
                                                formset=add_option_base_formset)


class add_facilitator_form(forms.ModelForm):
    email_id = forms.EmailField()
    first_name = forms.CharField(max_length=100, label="First name")

    class Meta:
        model = facilitator
        fields = ['first_name', 'middle_name', 'last_name', 'email_id', 'dob', 'occupation', 'password', 'mobile_number',
                  'address_1', 'languages', 'enroll_date', 'specified_interests', 'status', 'comments', 'gender', 'image']
        widgets = {
            # 'dob': forms.DateInput(format=('%m/%d/%Y'),attrs={'placeholder':'Select a date', 'type':'date'}),
            # 'enroll_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'comments': forms.Textarea, 'address_1': forms.Textarea}

    def __init__(self, *args, **kwargs):
        super(add_facilitator_form, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = entity_status.objects.filter(
            entity="Facilitator")

    def clean_mobile_number(self):
        mob = self.cleaned_data['mobile_number']
        if re.match(r'[6789]\d{9}$', mob):
            pass
        else:
            raise forms.ValidationError("The Mobile Number is not Valid")
        return mob

    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the Future!")
        return dob


class add_student_form(forms.ModelForm):
    email_id = forms.EmailField()

    class Meta:
        model = student
        fields = ['first_name', 'middle_name', 'last_name', 'email_id', 'dob', 'password', 'mobile_number',
                  'address_1', 'languages', 'enroll_date', 'gender', 'status', 'comments', 'image']
        widgets = {
            # 'dob': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            # 'enroll_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'comments': forms.Textarea, 'address_1': forms.Textarea}

    def __init__(self, *args, **kwargs):
        super(add_student_form, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = entity_status.objects.filter(
            entity="Student")

    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the Future!")
        return dob

    def clean_mobile_number(self):
        mob = self.cleaned_data['mobile_number']
        if re.match(r'[6789]\d{9}$', mob):
            pass
        else:
            raise forms.ValidationError("The Mobile Number is not Valid")
        return mob


class add_batch_form(forms.ModelForm):
    class Meta:
        model = batch
        fields = ['program_id', 'batch_name', 'start_date', 'end_date', 'status', 'partner_org',
                  'batch_incharge_id', 'center_id', 'student_count', 'sessions_count', 'comments']
        widgets = {
            # 'start_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            # 'end_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'comments': forms.Textarea}

    def __init__(self, *args, **kwargs):
        super(add_batch_form, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = entity_status.objects.filter(
            entity="Batch")
        # if self.instance:
        #     self.fields['status'].queryset = entity_status.objects.None()

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        # if end_date < datetime.date.today():
        #     raise forms.ValidationError("The date cannot be in the Past!")
        if end_date:
            if end_date <= start_date:
                raise forms.ValidationError(
                    "The End_date cannot be before Start_Date")
        return self.cleaned_data['end_date']


class password_facilitator_form(forms.ModelForm):
    class Meta:
        model = facilitator
        fields = ['password']


class password_student_form(forms.ModelForm):
    class Meta:
        model = student
        fields = ['password']


class add_center_form(forms.ModelForm):
    # email_id = forms.EmailField()
    class Meta:
        model = center
        fields = ['center_name', 'address_1', 'contact_person',
                  'mobile_number', 'email_id', 'center_type', 'comments']
        widgets = {'comments': forms.Textarea, 'address_1': forms.Textarea}

    def clean_mobile_number(self):
        mob = self.cleaned_data['mobile_number']
        if re.match(r'[6789]\d{9}$', mob):
            pass
        else:
            raise forms.ValidationError("The Mobile Number is not Valid")
        return mob
