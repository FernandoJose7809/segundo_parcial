from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from app.quater.models import Notes
from app.students.permissions import IsStudent
from rest_framework.permissions import IsAuthenticated
from app.grades.models import DegreeSubject
from .predictor import Prediccion
# Create your views here.

class PrediccionView(APIView):
<<<<<<< HEAD
    permission_classes = [IsStudent]
=======
    permission_classes =  [IsStudent]
>>>>>>> 1f72c9561e5ca7c954b7c6b755493b94fdbc4b9f
    
    def post(self, request):
        student = request.user.student
        degree_subject_id = request.data.get('degreeSubject')
        
        if not degree_subject_id:
            return Response({'error': 'Debe proporcionar degreeSubject'}, status=400)

        try:
            degree_subject = DegreeSubject.objects.get(id=degree_subject_id)
        except DegreeSubject.DoesNotExist:
            return Response({'error': 'DegreeSubject no encontrado'}, status=404)

        notes = Notes.getStudentNotes(student, degree_subject)
        year = student.actual_year()  # O el año del trimestre actual

        predictor = Prediccion()
        resultado = predictor.nota_final(
            year,
            notes['note_Participation'],
            notes['note_Task'],
            notes['note_Attendance'],
            notes['note_Exam'],
        )

        consejo = "Buen trabajo, sigue así." if resultado > 70 else "Necesitas mejorar tu participación y tareas."
        return Response({'prediccion': resultado, 'consejo': consejo})
