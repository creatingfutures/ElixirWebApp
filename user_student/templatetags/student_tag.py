from django import template


register = template.Library()



@register.filter
def index(List, i):
    return List[i].question

@register.filter
def index_img(List, i):
    return List[i].question.url

@register.filter
def index_av(List, i):
    return List[i].question.url

@register.filter
def index1_img(List, i):
    return List[i].option1.url

@register.filter
def index2_img(List, i):
    return List[i].option2.url

@register.filter
def index3_img(List, i):
    return List[i].option3.url

@register.filter
def index4_img(List, i):
    return List[i].option4.url

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
    if a=="av":
        return True
    else:
        return False
