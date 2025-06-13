from django.db import models
from app.students.models import Student


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
    degreeSubject = models.ForeignKey('grades.DegreeSubject', on_delete=models.CASCADE)
    quetar = models.ForeignKey(Quetar, on_delete=models.CASCADE)
    
    note_Task = models.FloatField(default=0)
    note_Exam = models.FloatField(default=0)
    note_Participation = models.FloatField(default=0)
    note_Attendance = models.FloatField(default=0)
    note = models.FloatField(default=0)

    @staticmethod
    def getStudentNotes(student,degreeSubject):
        notes = Notes.objects.filter(student=student,degreeSubject=degreeSubject).first()
        result= {
            'note_Task':notes.note_Task,
            'note_Participation':notes.note_Participation,
            'note_Exam':notes.note_Exam,
            'note_Attendance':notes.note_Attendance,
        }
        return result
    
    
# class FollowUp(models.Model):
#     type=models.CharField(max_length=1,choices=type_choices)
#     note_value=models.DecimalField(max_digits=5,decimal_places=2,default=0)
#     student=models.ForeignKey(Student,on_delete=models.SET_NULL,blank=True,null=True)
#     degreeSubject=models.ForeignKey('grades.DegreeSubject', on_delete=models.CASCADE)
#     note= models.ForeignKey(Notes,on_delete=models.CASCADE, blank=True, null=True)

# @receiver([post_save, post_delete], sender=FollowUp)
# def update_averages_on_followup_change(sender, instance, **kwargs):
#     from app.grades.models import DegreeSubject
#     degree_subject = instance.degreeSubject
#     grade = degree_subject.grade

#     followups = FollowUp.objects.filter(degreeSubject=degree_subject)
#     if followups.exists():
#         # Promedio de todas las notas (no solo exámenes)
#         degree_subject.average_Participation = followups.filter(type='P').aggregate(avg=Avg('note_value'))['avg'] or 0
#         degree_subject.average_attendance = followups.filter(type='A').aggregate(avg=Avg('note_value'))['avg'] or 0
#         degree_subject.average_tasks = followups.filter(type='T').aggregate(avg=Avg('note_value'))['avg'] or 0
#         degree_subject.average_exam = followups.filter(type='E').aggregate(avg=Avg('note_value'))['avg'] or 0
#         degree_subject.average_Note = followups.aggregate(avg=Avg('note'))['avg'] or 0
#         degree_subject.save()

#     all_degree_subjects = DegreeSubject.objects.filter(grade=grade)
#     if all_degree_subjects.exists():
#         grade.average_annual_grade = all_degree_subjects.aggregate(avg=Avg('average_Note'))['avg'] or 0
#         grade.average_annual_attendance = all_degree_subjects.aggregate(avg=Avg('average_attendance'))['avg'] or 0
#         grade.save()
        
class Attendance(models.Model):
    its_here = models.BooleanField(default=False)
    #student = models.ForeignKey(Student, on_delete=models.CASCADE,blank=True,null=True)
    #degreeSubject=models.ForeignKey('grades.DegreeSubject', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    note= models.ForeignKey(Notes,on_delete=models.CASCADE, blank=True, null=True)
    
class Task(models.Model):
    value = models.SmallIntegerField(default=0,blank=True)
    #student = models.ForeignKey(Student, on_delete=models.CASCADE,blank=True,null=True)
    #degreeSubject=models.ForeignKey('grades.DegreeSubject', on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    note= models.ForeignKey(Notes,on_delete=models.CASCADE, blank=True, null=True)
    url = models.URLField(blank=True,null=True)
    end_date = models.DateField()

class Participation(models.Model):
    value = models.SmallIntegerField(default=0,blank=True)
    #student = models.ForeignKey(Student, on_delete=models.CASCADE,blank=True,null=True)
    #degreeSubject=models.ForeignKey('grades.DegreeSubject', on_delete=models.CASCADE)
    note= models.ForeignKey(Notes,on_delete=models.CASCADE, blank=True, null=True)
    
class Exam(models.Model):
    value = models.SmallIntegerField(default=0,blank=True)
    #student = models.ForeignKey(Student, on_delete=models.CASCADE,blank=True,null=True)
    #degreeSubject=models.ForeignKey('grades.DegreeSubject', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    note= models.ForeignKey(Notes,on_delete=models.CASCADE, blank=True, null=True)
    
    
        
# class TareaUrl(models.Model):
#     url = models.URLField(blank=True,null=True)
#     task = models.ForeignKey(Task,on_delete=models.CASCADE)