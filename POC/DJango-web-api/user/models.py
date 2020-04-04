from django.db import models


class employee(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    emp_id = models.IntegerField()
