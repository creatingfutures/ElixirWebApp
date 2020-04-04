from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
@login_required
def home(request):
    return render(request,'home.html')
