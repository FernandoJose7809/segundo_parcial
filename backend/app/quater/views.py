from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Quetar, Notes, Attendance,Task, Exam, Participation
from .serializers import QuetarSerializer, NotesSerializer, AttendanceSerializer,TaskSerializer, ExamSerializer,ParticipationSerializer
from app.grades.models import StudentCourse, DegreeSubject
from app.teacher.permissions import IsTeacher
from datetime import date

# #!Eliminar
from django.db.models.signals import post_save
from django.dispatch import receiver
# #!Eliminar

# Create your views here...
class QuetarViewSet(viewsets.ModelViewSet):
    queryset = Quetar.objects.all()
    serializer_class = QuetarSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        quetar = self.serializer_class.Meta.model.objects.get(pk=response.data['id'])
        for degreeSubject in DegreeSubject.objects.all():
            student_courses = StudentCourse.objects.filter(grade=degreeSubject.grade)
            for sc in student_courses:
                Notes.objects.get_or_create(
                    student=sc.student,
                    degreeSubject=degreeSubject,
                    quetar=quetar
                )
        return response
    
# #!ELINAR 
# @receiver(post_save, sender=Quetar)
# def crear_notes_automaticamente(sender, instance, created, **kwargs):
#     if created:
#         print("Se creó un Quarter desde cualquier lugar")
#         for degreeSubject in DegreeSubject.objects.all():
#             student_courses = StudentCourse.objects.filter(grade=degreeSubject.grade)
#             for sc in student_courses:
#                 Notes.objects.get_or_create(
#                     student=sc.student,
#                     degreeSubject=degreeSubject,
#                     quetar=instance
#                 )
# #!ELINAR


# class FollowUpViewSet(viewsets.ModelViewSet):
#     #queryset = FollowUp.objects.all()
#     serializer_class = FollowUpSerializer
#     #permission_classes = [IsTeacher]
    
#     def create(self, request, *args, **kwargs):
#         t = request.data.get('type')
#         try:
#             degreeSubject = request.data.get('degreeSubject')
#             courses = StudentCourse.objects.filter(grade=degreeSubject.grade)
#             students = [course.student for course in courses]
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         if t == 'T':
#             try:
#                 date_end = request.data.get('date_end')
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#             try:
#                 if date.fromisoformat(date_end) < date.today():
#                     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#         quetar = Quetar.getQuetar(date.today())

#         for student in students:
#             try:
#                 note = Notes.objects.get(
#                     student=student,
#                     degreeSubject=degreeSubject,
#                     quetar=quetar
#                 )
#             except Notes.DoesNotExist:
#                 return Response({
#                     'error': f'No se encontró una nota para {student} en {degreeSubject} y quetar {quetar}'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             followUp = FollowUp.objects.create(
#                 type=t,
#                 note_value=0,
#                 student=student,
#                 degreeSubject=degreeSubject,
#                 note=note
#             )
        
#             if t == 'T':
#                 TareaUrl.objects.create(
#                     url=None,
#                     followUp=followUp,
#                     end_date=date_end
#                 )
                
#     def get_queryset(self):
#         grade_id = self.request.query_params.get('grade_id')
#         if not grade_id:
#             return FollowUp.objects.none()
#         return FollowUp.objects.filter(degreeSubject__grade_id=grade_id)
    
#     def perform_update(self, serializer):
#         instance = serializer.save()
#         instance.note.recalculate()
#         instance.degreeSubject.recalculate()



class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()

    def perform_create(self, serializer):
        degree_subject = self.request.data.get('degreeSubject')
        if not degree_subject:
            raise serializers.ValidationError("Debe enviar degreeSubject")

        try:
            ds = DegreeSubject.objects.get(id=degree_subject)
        except DegreeSubject.DoesNotExist:
            raise serializers.ValidationError("DegreeSubject inválido")

        quetar = Quetar.getQuetar()
        note = Notes.objects.filter(degreeSubject=ds, quetar=quetar).first()
        if not note:
            raise serializers.ValidationError("No se encontró Note para esa combinación")

        serializer.save(note=note)
@receiver(post_save, sender=Attendance)
def actualizar_attendance(sender, instance, **kwargs):
    if instance.note:
        # Obtener todas las asistencias asociadas a esa nota
        attendances = Attendance.objects.filter(note=instance.note)
        total = 0
        for att in attendances:
            total += 100 if att.its_here else 0

        promedio = total / attendances.count() if attendances.exists() else 0
        instance.note.note_Attendance = round(promedio, 2)
        instance.note.save()
        
        calcular_promedio_final(instance.note)
            

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        degree_subject = self.request.data.get('degreeSubject')
        if not degree_subject:
            raise serializers.ValidationError("Debe enviar degreeSubject")

        try:
            ds = DegreeSubject.objects.get(id=degree_subject)
        except DegreeSubject.DoesNotExist:
            raise serializers.ValidationError("DegreeSubject inválido")

        quetar = Quetar.getQuetar()
        note = Notes.objects.filter(degreeSubject=ds, quetar=quetar).first()
        if not note:
            raise serializers.ValidationError("No se encontró Note para esa combinación")

        serializer.save(note=note)
@receiver(post_save, sender=Task)
def actualizar_task(sender, instance, **kwargs):
    if instance.note:
        # Obtener todas las tareas asociadas a esa nota
        tasks = Task.objects.filter(note=instance.note)
        total = 0
        for t in tasks:
            total += t.value

        promedio = total / tasks.count() if tasks.exists() else 0

        instance.note.note_Task = round(promedio, 2)
        instance.note.save()
        calcular_promedio_final(instance.note)

            
        
        
class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()

    def perform_create(self, serializer):
        degree_subject = self.request.data.get('degreeSubject')
        if not degree_subject:
            raise serializers.ValidationError("Debe enviar degreeSubject")

        try:
            ds = DegreeSubject.objects.get(id=degree_subject)
        except DegreeSubject.DoesNotExist:
            raise serializers.ValidationError("DegreeSubject inválido")

        quetar = Quetar.getQuetar()
        note = Notes.objects.filter(degreeSubject=ds, quetar=quetar).first()
        if not note:
            raise serializers.ValidationError("No se encontró Note para esa combinación")

        serializer.save(note=note)
@receiver(post_save, sender=Exam)
def actualizar_exam(sender, instance, **kwargs):
    if instance.note:
        exams = Exam.objects.filter(note=instance.note)
        total = 0
        for e in exams:
            total += e.value

        promedio = total / exams.count() if exams.exists() else 0

        instance.note.note_Exam = round(promedio, 2)
        instance.note.save()
        calcular_promedio_final(instance.note)

        
class ParticipationViewSet(viewsets.ModelViewSet):
    serializer_class = ParticipationSerializer
    queryset = Participation.objects.all()

    def perform_create(self, serializer):
        degree_subject = self.request.data.get('degreeSubject')
        if not degree_subject:
            raise serializers.ValidationError("Debe enviar degreeSubject")

        try:
            ds = DegreeSubject.objects.get(id=degree_subject)
        except DegreeSubject.DoesNotExist:
            raise serializers.ValidationError("DegreeSubject inválido")

        quetar = Quetar.getQuetar()
        note = Notes.objects.filter(degreeSubject=ds, quetar=quetar).first()
        if not note:
            raise serializers.ValidationError("No se encontró Note para esa combinación")

        serializer.save(note=note)
@receiver(post_save, sender=Participation)
def actualizar_participation(sender, instance, **kwargs):
    if instance.note:
        participations = Participation.objects.filter(note=instance.note)
        total = 0
        for p in participations:
            total += p.value

        promedio = total / participations.count() if participations.exists() else 0

        instance.note.note_Participation = round(promedio, 2)
        instance.note.save()
        calcular_promedio_final(instance.note)


    
                     


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    
def calcular_promedio_final(note):
    note.note = (
        note.note_Task * 0.15 +
        note.note_Exam * 0.60 +
        note.note_Participation * 0.10 +
        note.note_Attendance * 0.15
    )