from django.db import models
from app.students.models import Student
from app.grades.models import DegreeSubject

# Create your models here.
type_choices=[
        ('A', 'Asistencia'),
        ('T', 'Tarea'),
        ('P', 'Participacion'),
        ('E', 'Examen'),
    ]
class Quetar(models.Model):
    description=models.CharField(max_length=255,blank=True,null=True)
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    
class FollowUp(models.Model):
    type=models.CharField(max_length=1,choices=type_choices)
    note=models.DecimalField(max_digits=5,decimal_places=2)
    student=models.ForeignKey(Student,on_delete=models.SET_NULL,null=True)
    degreeSubject=models.ForeignKey(DegreeSubject, on_delete=models.CASCADE)
    quetar=models.ForeignKey(Quetar,on_delete=models.SET_NULL,null=True)