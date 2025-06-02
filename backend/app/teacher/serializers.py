from rest_framework import serializers
from .models import *
from app.subjects.models import Subject

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'
        
class TeacherSubjectSerializer(serializers.ModelSerializer):
    teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    
    class Meta:
        model=TeacherSubject
        fields='__all__'
        
