from rest_framework import serializers
from .models import employee


# class employeeSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model=employee
#         fields=('firstname','emp_id')


class employeeSerializer(serializers.ModelSerializer):

    class Meta:
        model=employee
        fields=['firstname','emp_id']
