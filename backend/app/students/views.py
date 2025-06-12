from django.shortcuts import render
from rest_framework import viewsets
from .models import Student, Tutor
from .serializers import StudentSerializer, TutorSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
