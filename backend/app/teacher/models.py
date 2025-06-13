from django.db import models
from django.contrib.auth.models import User
from app.subjects.models import Subject
from datetime import datetime

# Create your models here.

class Teacher(models.Model):
    gener_choices=[
        ('M', 'Masculino'),
        ('F','Femenino'),
    ]
    ci = models.IntegerField()
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    birthdate=models.DateField()
    gender=models.CharField(max_length=1,choices=gener_choices)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    user=models.ForeignKey(User,related_name='teacher',
                           on_delete=models.SET_NULL,blank=True,null=True)
    created_year = models.IntegerField(default=datetime.now().year)
    

class TeacherSubject(models.Model):
    teacher=models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    