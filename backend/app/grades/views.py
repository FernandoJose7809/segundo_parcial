# app/courses/views.py
from rest_framework import viewsets
from .models import Grade, StudentCourse, DegreeSubject, GroupTeacher
from .serializers import GradeSerializer, StudentCourseSerializer, DegreeSubjectSerializer, GroupTeacherSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class StudentCourseViewSet(viewsets.ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer

class DegreeSubjectViewSet(viewsets.ModelViewSet):
    queryset = DegreeSubject.objects.all()
    serializer_class = DegreeSubjectSerializer

class GroupTeacherViewSet(viewsets.ModelViewSet):
    queryset = GroupTeacher.objects.all()
    serializer_class = GroupTeacherSerializer
