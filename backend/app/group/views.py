from django.shortcuts import render
from rest_framework import viewsets
from .models import Group,GroupTeacher
from .serializers import GroupSerializer,GroupTeacherSerializer
# Create your views here.

class GroupViewSet(viewsets.ModelViewSet):
    queryset=Group.objects.all()
    serializer_class=GroupSerializer

class GroupTeacherViewSet(viewsets.ModelViewSet):
    queryset=GroupTeacher.objects.all()
    serializer_class=GroupTeacherSerializer
