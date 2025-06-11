from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Student(models.Model):
    gener_choices=[
        ('M', 'Masculino'),
        ('F','Femenino'),
    ]
    ci = models.IntegerField()
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    birthdate=models.DateField()
    gender=models.CharField(max_length=1,choices=gener_choices)
    address = models.CharField(max_length=100, null=True, blank=True)
    student_phone=models.CharField(max_length=15,blank=True,null=True)
    parent_phone=models.CharField(max_length=15)
    student_email=models.EmailField(unique=True)
    user=models.ForeignKey(User,related_name='student',
                           on_delete=models.SET_NULL,blank=True,null=True)
    created_year = models.IntegerField(default=datetime.now().year)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def actual_year(self):
        from app.grades.models import StudentCourse
        student_courses = StudentCourse.objects.filter(student=self).select_related('grade')
        for course in student_courses:
            if course.grade.year == datetime.now().year:
                return int(course.grade.grade) 
        return None
    