from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import employee
from rest_framework import viewsets
from .serializers import employeeSerializer
import MySQLdb

# Create your views here.

def home(request):
    db = MySQLdb.connect(user='root', db='dbname', passwd='root', host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM student')
    names = [row[0] for row in cursor.fetchall()]
    db.close()
    e=employee.objects.all()
    for i in e:
        names.append()
    return render(request, 'home.html', {'emp': names})


# class employeeList(viewsets.ModelViewSet):
#     employees=employee.objects.all()
#     serializer=employeeSerializer

class employeeList(APIView):
    def get(self,request):
        employees=employee.objects.all()
        serializer=employeeSerializer(employees,many=True)
        return Response(serializer.data)

@api_view(('GET',))
def employee_view(request):
    if request.method=="GET":
        employees=employee.objects.all()
        serializer=employeeSerializer(employees,many=True)
        return Response(serializer.data)

@api_view(('PUT',))
def employee_update(request,id):
    if request.method=="PUT":
        employees=get_object_or_404(employee,emp_id=id)
        serializer=employeeSerializer(employees,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data["Success"]="DONE"
            return Response(data=data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(('POST',))
def employee_create(request):
    if request.method=="POST":
        a=request.data['firstname']
        e=employee(firstname=a)
        serializer=employeeSerializer(e,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data["Success"]="DONE"
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
