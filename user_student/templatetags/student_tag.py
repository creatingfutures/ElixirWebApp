from django import template
from django.core import serializers
from user_admin.models import *

register = template.Library()

@register.filter
def get_dictionary_item(dictionary,key):
    return dictionary.get(key)

@register.filter
def add_str(string,strToAdd):
    return str(string)+'-'+str(strToAdd)

@register.filter
def prefix(a):
    distinct = []
    for i in question.objects.filter(level_id=a):
        if(i.assessment_type_id!=None):
            if(i.assessment_type_id in distinct):
                pass
            else:
                distinct.append(i.assessment_type_id)
    print(distinct,assessment_type.objects.filter(assessment_type_id__in=distinct))
    return assessment_type.objects.filter(assessment_type_id__in=distinct)

@register.filter
def get_hint(List,i):
    L = list(serializers.deserialize("json",List))
    print('hint only',L[i].object.hint)
    if(L[i].object.hint == ''):
        print('None')
        return 'None'
    else:
        return L[i].object.hint

@register.filter
def index(List, i):
    L = list(serializers.deserialize("json",List))
    return L[i].object.question

@register.filter
def index_narrative(List, i):
    L = list(serializers.deserialize("json",List))
    return L[i].object.narrative

@register.filter
def getObject(List, i):
    if not isinstance(List,list):
     L = list(serializers.deserialize("json",List))
    else:
     L=List 
    return L[i].object


@register.filter
def index_img(List, i):
    L = list(serializers.deserialize("json",List))
    return L[i].object.content

@register.filter
def index_av(List, i):
    L = list(serializers.deserialize("json",List))
    return L[i].object.content

@register.filter
def index1_img(List, i):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=1:
        return L[i].object.options[0]
    else:
        return ""

@register.filter
def index2_img(List, i):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=2:
        return L[i].object.options[1]
    else:
        return ""

@register.filter
def index3_img(List, i):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=3:
            return L[i].object.options[2]
    else:
            return ""

@register.filter
def index4_img(List, i):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=4:
        return L[i].object.options[3]
    else:
        return ""

@register.filter
def index1(List, i):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=1:
        return L[i].object.options[0]
    else:
        return ""

@register.filter
def index2(List, i):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=2:
        return L[i].object.options[1]
    else:
        return ""

@register.filter
def index3(List, i):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=3:
        return L[i].object.options[2]
    else:
        return ""

@register.filter
def index4(List, i):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=4:
        return L[i].object.options[3]
    else:
        return ""

@register.filter
def indexn(List, i,n):
    L = list(serializers.deserialize("json",List))
    if len(L[i].object.options)>=n:
        return L[i].object.options[n-1]
    else:
        return ""

@register.filter
def index5(List, i):
    L = list(serializers.deserialize("json",List))
    return L[i].object.answer


@register.filter
def id(List, i):
    return List[i]

@register.filter
def str1(arg1):
    return str(arg1)+".jpg"

@register.filter
def allcaps(str1):
    return str1.upper()

@register.filter
def get1(a):
    return a

@register.filter
def standard(a):
    if a=="standard":
        return True
    else:
        return False

@register.filter
def image(a):
    if a=="image":
        return True
    else:
        return False

@register.filter
def av(a):
    if a=="av_test":
        return True
    else:
        return False