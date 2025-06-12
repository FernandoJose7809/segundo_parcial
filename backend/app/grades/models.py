from django.db import models
from app.students.models import Student
from app.subjects.models import Subject
from app.teacher.models import TeacherSubject
from app.quater.models import Notes
from datetime import datetime
# Create your models here.

class Grade(models.Model):
    year = models.IntegerField(default = datetime.now().year)
    grade = models.CharField(max_length=1)
    acronym = models.CharField(max_length=2)
    average_annual_grade = models.DecimalField(max_digits=5, decimal_places=2,
                                             null=True, blank=True, default=0)
    average_annual_attendance = models.DecimalField(max_digits=5, decimal_places=2,
                                                  null=True, blank=True, default=0)
    
    def __str__(self):
        return f"{self.grade} - {self.year}"
    
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    is_repeater = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('student', 'grade')
        
    def __str__(self):
        return f"{self.student} - {self.grade} ({'Repite' if self.is_repeater else 'Normal'})"
    
class DegreeSubject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    average_Participation = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                      blank=True, default=0)
    average_attendance = models.DecimalField(max_digits=5,decimal_places=2,
                                           null=True, blank=True, default=0)
    average_tasks = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                      blank=True, default=0)
    average_exam = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                      blank=True, default=0)
    average_Note = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                      blank=True, default=0)
    state = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('grade','subject')
        
    def recalculate(self):
        notes = Notes.objects.filter(degreeSubject=self)

        avg_attendance = 0
        avg_participation = 0
        avg_tasks = 0
        avg_exam = 0
        avg_note = 0
        count = notes.count()

        for note in notes:
            avg_attendance += note.average_attendance or 0
            avg_participation += note.average_Participation or 0
            avg_tasks += note.average_tasks or 0
            avg_exam += note.average_exam or 0
            avg_note += note.average_Note or 0

        if count > 0:
            self.average_attendance = avg_attendance / count
            self.average_Participation = avg_participation / count
            self.average_tasks = avg_tasks / count
            self.average_exam = avg_exam / count
            self.average_Note = avg_note / count
            self.save()


        
        
class GroupTeacher(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    teacherSubject = models.ForeignKey(TeacherSubject, on_delete=models.SET_NULL, null=True)