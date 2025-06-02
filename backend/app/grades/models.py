from django.db import models
from app.students.models import Student
from app.subjects.models import Subject
from datetime import datetime
# Create your models here.

class Grade(models.Model):
    year=models.IntegerField(default=datetime.now().year)
    grade=models.CharField(max_length=1)
    average_annual_grade=models.DecimalField(max_digits=5,decimal_places=2,
                                             null=True,blank=True)
    average_annual_attendance=models.DecimalField(max_digits=5,decimal_places=2
                                                  ,null=True,blank=True)
    
    def __str__(self):
        return f"{self.grade} - {self.year}"
    
class StudentCourse(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    grade=models.ForeignKey(Grade,on_delete=models.CASCADE)
    is_repeater = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('student', 'grade')
        
    def __str__(self):
        return f"{self.student} - {self.grade} ({'Repite' if self.is_repeater else 'Normal'})"
    
class DegreeSubject(models.Model):
    grade=models.ForeignKey(Grade,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    average_grade=models.DecimalField(max_digits=5,decimal_places=2,null=True,
                                      blank=True)
    average_attendance=models.DecimalField(max_digits=5,decimal_places=2,
                                           null=True,blank=True)
    average_tasks=models.DecimalField(max_digits=5,decimal_places=2,null=True,
                                      blank=True)
    average_exam=models.DecimalField(max_digits=5,decimal_places=2,null=True,
                                      blank=True)
    average_Note=models.DecimalField(max_digits=5,decimal_places=2,null=True,
                                      blank=True)
    state=models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('grade','subject')