from rest_framework import serializers
from .models import Group,GroupTeacher
from app.grades.models import Grade
from app.teacher.models import TeacherSubject

class GroupSerializer(serializers.ModelSerializer):
    grade=serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())
    
    class Meta:
        model=Group
        fields='__all__'
        
class GroupTeacherSerializer(serializers.ModelSerializer):
    group=serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    teacherSubject=serializers.PrimaryKeyRelatedField(queryset=TeacherSubject.objects.all())
    
    class Meta:
        model=GroupTeacher
        fields='__all__'