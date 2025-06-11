from django.db import models
from app.students.models import Student
from app.grades.models import DegreeSubject
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.grades.models import DegreeSubject, Grade
from django.db.models import Avg

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

@receiver([post_save, post_delete], sender=FollowUp)
def update_averages_on_followup_change(sender, instance, **kwargs):
    degree_subject = instance.degreeSubject
    grade = degree_subject.grade

    followups = FollowUp.objects.filter(degreeSubject=degree_subject)
    if followups.exists():
        # Promedio de todas las notas (no solo exámenes)
        degree_subject.average_grade = followups.aggregate(avg=Avg('note'))['avg'] or 0
        degree_subject.average_attendance = followups.filter(type='A').aggregate(avg=Avg('note'))['avg'] or 0
        degree_subject.average_tasks = followups.filter(type='T').aggregate(avg=Avg('note'))['avg'] or 0
        degree_subject.average_exam = followups.filter(type='E').aggregate(avg=Avg('note'))['avg'] or 0
        degree_subject.average_Note = followups.aggregate(avg=Avg('note'))['avg'] or 0
        degree_subject.save()

    all_degree_subjects = DegreeSubject.objects.filter(grade=grade)
    if all_degree_subjects.exists():
        grade.average_annual_grade = all_degree_subjects.aggregate(avg=Avg('average_grade'))['avg'] or 0
        grade.average_annual_attendance = all_degree_subjects.aggregate(avg=Avg('average_attendance'))['avg'] or 0
        grade.save()