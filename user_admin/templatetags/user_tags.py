from django import template


register = template.Library()

@register.filter
def index(List, i):
    return List[i]

@register.filter
def index1(List):
    return List["modules"]


@register.filter
def index2(List):
    return List[0].program_id.program_id

@register.filter
def index3(List):
    return List["facilitators"]



@register.filter
def check(int):
    if int>0:
        return True;
    else:
        return False

@register.filter
def check1(list):
    if len(list)>0:
        return True;
    else:
        return False

@register.filter
def check_av(list):
    if list=="Video":
        return True
    else:
        return False
