from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Tutor
from .serializers import StudentSerializer, TutorSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        student = Student.objects.filter(user=user).first()
        if student:
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        return Response({'detail': 'No existe estudiante para este usuario.'}, status=404)

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
