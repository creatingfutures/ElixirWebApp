from django import template


register = template.Library()



@register.filter
def index(List, i):
    return List[i].question

@register.filter
def index1(List, i):
    return List[i].option1

@register.filter
def index2(List, i):
    return List[i].option2

@register.filter
def index3(List, i):
    return List[i].option3

@register.filter
def index4(List, i):
    return List[i].option4

@register.filter
def index5(List, i):
    return List[i].answer
