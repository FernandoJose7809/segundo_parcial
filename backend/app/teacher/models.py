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
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    birthdate=models.DateField()
    gender=models.CharField(max_length=1,choices=gener_choices)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    user=models.ForeignKey(User,related_name='teacher',
                           on_delete=models.SET_NULL,blank=True,null=True)
    created_year = models.IntegerField(default=datetime.now().year)
    

class TeacherSubject(models.Model):
    teacher=models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    