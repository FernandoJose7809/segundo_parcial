from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Quetar, FollowUp, TareaUrl, Notes
from .serializers import QuetarSerializer, FollowUpSerializer, TareaUrlSerializer, NotesSerializer
from app.grades.models import StudentCourse, DegreeSubject
from app.teacher.permissions import IsTeacher
from datetime import date

# #!Eliminar
# from django.db.models.signals import post_save
# from django.dispatch import receiver
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


class FollowUpViewSet(viewsets.ModelViewSet):
    #queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer
    permission_classes = [IsTeacher]
    
    def create(self, request, *args, **kwargs):
        t = request.data.get('type')
        try:
            degreeSubject_id = request.data.get('degreeSubject_id')
            degreeSubject = DegreeSubject.objects.get(id=degreeSubject_id)
            courses = StudentCourse.objects.filter(grade=degreeSubject.grade)
            students = [course.student for course in courses]
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if t == 'T':
            try:
                date_end = request.data.get('date_end')
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            try:
                if date.fromisoformat(date_end) < date.today():
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        quetar = Quetar.getQuetar(date.today())

        for student in students:
            try:
                note = Notes.objects.get(
                    student=student,
                    degreeSubject=degreeSubject,
                    quetar=quetar
                )
            except Notes.DoesNotExist:
                return Response({
                    'error': f'No se encontró una nota para {student} en {degreeSubject} y quetar {quetar}'
                }, status=status.HTTP_400_BAD_REQUEST)

            followUp = FollowUp.objects.create(
                type=t,
                note_value=0,
                student=student,
                degreeSubject=degreeSubject,
                note=note
            )
        
            if t == 'T':
                TareaUrl.objects.create(
                    url=None,
                    followUp=followUp,
                    end_date=date_end
                )
                
    def get_queryset(self):
        grade_id = self.request.query_params.get('grade_id')
        if not grade_id:
            return FollowUp.objects.none()
        return FollowUp.objects.filter(degreeSubject__grade_id=grade_id)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.note.recalculate()
        instance.degreeSubject.recalculate()
              
                 
class TareaUrlViewSet(viewsets.ModelViewSet):
    queryset = TareaUrl.objects.all()
    serializer_class = TareaUrlSerializer


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer