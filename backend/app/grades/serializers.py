from rest_framework import serializers
from .models import Grade,StudentCourse,DegreeSubject, GroupTeacher
from app.students.models import Student
from app.subjects.models import Subject
from app.teacher.models import TeacherSubject

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class StudentCourseSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())

    class Meta:
        model = StudentCourse
        fields = '__all__'


class DegreeSubjectSerializer(serializers.ModelSerializer):
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), allow_null=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = DegreeSubject
        fields = '__all__'

class GroupTeacherSerializer(serializers.Serializer):
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())
    teacherSubject = serializers.PrimaryKeyRelatedField(queryset=TeacherSubject.objects.all())
    
    class Meta:
        model = GroupTeacher
        fields = '__all__'