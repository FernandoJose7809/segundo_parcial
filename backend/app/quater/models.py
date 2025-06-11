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
    queter=models.CharField(max_length=1,choices=[('1','1'),('2','2'),('3','3')])
    description=models.CharField(max_length=255,blank=True,null=True)
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    
    @staticmethod
    def getQuetar(date):
        return Quetar.objects.filter(start_date__lte=date, end_date__gte=date).first()
    

class Notes(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    degreeSubject = models.ForeignKey(DegreeSubject, on_delete=models.CASCADE)
    quetar = models.ForeignKey(Quetar, on_delete=models.CASCADE)
    
    note_Task = models.FloatField(default=0)
    note_Exam = models.FloatField(default=0)
    note_Participation = models.FloatField(default=0)
    note_Attendance = models.FloatField(default=0)
    note = models.FloatField(default=0)

    def recalculate(self):
        followups = FollowUp.objects.filter(note=self)

        tipos = {
            'T': {'total': 0, 'count': 0},
            'E': {'total': 0, 'count': 0},
            'P': {'total': 0, 'count': 0},
            'A': {'total': 0, 'count': 0},
        }

        for f in followups:
            if f.type in tipos:
                tipos[f.type]['total'] += f.note_value
                tipos[f.type]['count'] += 1

        self.note_Task = tipos['T']['total'] / tipos['T']['count'] if tipos['T']['count'] > 0 else 0
        self.note_Exam = tipos['E']['total'] / tipos['E']['count'] if tipos['E']['count'] > 0 else 0
        self.note_Participation = tipos['P']['total'] / tipos['P']['count'] if tipos['P']['count'] > 0 else 0
        self.note_Attendance = tipos['A']['total'] / tipos['A']['count'] if tipos['A']['count'] > 0 else 0

        self.note = (
            self.note_Task * 0.15 +
            self.note_Exam * 0.60 +
            self.note_Participation * 0.10 +
            self.note_Attendance * 0.15
        )
        self.save()

    @staticmethod
    def getStudentNotes(student:Student,degreeSubject:DegreeSubject):
        #Crear una nueva fucion y filtar segun el trimestre que este cursando
        notes = Notes.objects.filter(student=student,degreeSubject=degreeSubject).first()
        result= {
            'note_Task':notes.note_Task,
            'note_Participation':notes.note_Participation,
            'note_Exam':notes.note_Exam,
            'note_Attendance':notes.note_Attendance,
        }
        return result
    
    
class FollowUp(models.Model):
    type=models.CharField(max_length=1,choices=type_choices)
    note_value=models.DecimalField(max_digits=5,decimal_places=2,)
    student=models.ForeignKey(Student,on_delete=models.SET_NULL,blank=True,null=True)
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
