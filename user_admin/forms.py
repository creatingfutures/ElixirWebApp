from django import forms

from .models import program,program_module,facilitator,center
from .models import student,module_level,questions,batch
import datetime
import re

class add_program_form(forms.ModelForm):
    class Meta:
        model=program
        fields=['program_name','prerequisite','comments']
        widgets={'comments':forms.Textarea}

class add_module_form(forms.ModelForm):
    class Meta:
        model = program_module
        fields=['module_name']
    def clean_module_name(self):
        m=self.instance.program_id
        l=self.cleaned_data['module_name']
        ls=program_module.objects.filter(program_id=m)
        for i in ls:
            if i==self.instance:
                continue
            if l == i.module_name:
                raise forms.ValidationError("A module with that name already exists for this program")
        return l

class add_level_form(forms.ModelForm):
    class Meta:
        model = module_level
        fields=['level_number','level_description']

    def clean_level_number(self):
        m=self.instance.module_id
        l=self.cleaned_data['level_number']
        ls=module_level.objects.filter(module_id=m)
        for i in ls:
            if i == self.instance:
                continue
            if l == i.level_number:
                raise forms.ValidationError("A level with that number already exists for this module")
        return l

    def clean_level_description(self):
        m=self.instance.module_id
        l=self.cleaned_data['level_description']
        ls=module_level.objects.filter(module_id=m)
        for i in ls:
            if i == self.instance:
                continue
            if l == i.level_description:
                raise forms.ValidationError("A level with that description already exists for this module")
        return l

class add_question_form(forms.ModelForm):
    class Meta:
        model = questions
        fields=['question','answer','program_id'
        ,'module_id','level_id','question_type',
        'option1','option2','option3','option4','comments']
        widgets={'comments':forms.Textarea}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['module_id'].queryset = program_module.objects.none()
        self.fields['level_id'].queryset = module_level.objects.none()

        if 'program_id' in self.data:
            try:
                program_id = int(self.data.get('program_id'))
                self.fields['module_id'].queryset = program_module.objects.filter(program_id=program_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['module_id'].queryset = self.instance.program_id.program_module_set

        if 'module_id' in self.data:
            try:
                module_id = int(self.data.get('module_id'))
                self.fields['level_id'].queryset = module_level.objects.filter(module_id=module_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['level_id'].queryset = self.instance.module_id.module_level_set




class add_facilitator_form(forms.ModelForm):
    email_id = forms.EmailField()
    first_name = forms.CharField(max_length=100,label="First name")

    class Meta:
        model=facilitator
        fields=['first_name','middle_name','last_name','email_id','dob','occupation','password','mobile_number',
        'address_1','languages','enroll_date','specified_interests','status','comments','image']
        widgets = {
        'dob': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'enroll_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'comments':forms.Textarea,'address_1':forms.Textarea}
    def clean_mobile_number(self):
        mob = self.cleaned_data['mobile_number']
        if re.match(r'[789]\d{9}$',mob):
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
        model=student
        fields=['first_name','middle_name','last_name','email_id','dob','password','mobile_number',
        'address_1','languages','enroll_date','gender','status','comments','image']
        widgets = {
        'dob': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'enroll_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'comments':forms.Textarea,'address_1':forms.Textarea}
    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the Future!")
        return dob
    def clean_mobile_number(self):
        mob = self.cleaned_data['mobile_number']
        if re.match(r'[789]\d{9}$',mob):
            pass
        else:
            raise forms.ValidationError("The Mobile Number is not Valid")
        return mob

class add_batch_form(forms.ModelForm):
    class Meta:
        model=batch
        fields=['program_id','batch_name','start_date','end_date','status','partner_org','batch_incharge_id','center_id'
        ,'student_count','sessions_count','comments']
        widgets = {
        'start_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'end_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'comments':forms.Textarea}
    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date=self.cleaned_data['start_date']
        if end_date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the Past!")
        elif end_date<=start_date:
            raise forms.ValidationError("The End_date cannot be before Start_Date")
        return end_date


class password_facilitator_form(forms.ModelForm):
    class Meta:
        model=facilitator
        fields=['password']

class password_student_form(forms.ModelForm):
    class Meta:
        model=student
        fields=['password']

class add_center_form(forms.ModelForm):
    email_id = forms.EmailField()
    class Meta:
        model = center
        fields=['center_name','address_1','contact_person','mobile_number','email_id','center_type','comments']
        widgets={'comments':forms.Textarea,'address_1':forms.Textarea}

    def clean_mobile_number(self):
        mob = self.cleaned_data['mobile_number']
        if re.match(r'[789]\d{9}$',mob):
            pass
        else:
            raise forms.ValidationError("The Mobile Number is not Valid")
        return mob
