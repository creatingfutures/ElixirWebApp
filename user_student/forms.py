from django import forms
from user_student.models import skillmaster

class NameForm(forms.Form):
    mcv_statement = forms.CharField(label='mcv_statement', max_length=100)
    new_job = forms.CharField(label='new_job', max_length=100)
    new_edu = forms.CharField(label='new_edu', max_length=100)
    new_train = forms.CharField(label='new_train', max_length=100)
    new_qualites = forms.CharField(label='new_qualites', max_length=100)
    new_hard = forms.CharField(label='new_hard', max_length=100)
    new_talent = forms.CharField(label='new_talent', max_length=100)
    
