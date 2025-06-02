from rest_framework import viewsets
from .models import Teacher,TeacherSubject
from .serializers import TeacherSerializer,TeacherSubjectSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer

