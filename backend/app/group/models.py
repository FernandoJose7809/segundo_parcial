from django.db import models
from app.grades.models import Grade
from app.teacher.models import TeacherSubject
# Create your models here.
class Group(models.Model):
    sigla=models.CharField(max_length=2)
    grade=models.ForeignKey(Grade,on_delete=models.CASCADE)
    
class GroupTeacher(models.Model):
    group=models.ForeignKey(Group,on_delete=models.SET_NULL,null=True)
    teacherSubject=models.ForeignKey(TeacherSubject,on_delete=models.SET_NULL,null=True)