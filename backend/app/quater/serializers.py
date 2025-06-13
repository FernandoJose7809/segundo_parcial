from rest_framework import serializers
from .models import Quetar,TareaUrl, Notes, Task, Attendance, Exam,Participation #,FollowUp
from app.students.models import Student
from app.grades.models import DegreeSubject

class QuetarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quetar
        fields = '__all__'


# class FollowUpSerializer(serializers.ModelSerializer):
#     student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
#     degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())
#     note = serializers.PrimaryKeyRelatedField(queryset=Notes.objects.all())

#     class Meta:
#         model = FollowUp
#         fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    #student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    #degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())
    note = serializers.PrimaryKeyRelatedField(queryset=Notes.objects.all())
    class Meta:
        model = Attendance
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    #student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    #degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())
    note = serializers.PrimaryKeyRelatedField(queryset=Notes.objects.all())
    class Meta:
        model = Task
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    #student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    #degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())
    note = serializers.PrimaryKeyRelatedField(queryset=Notes.objects.all())
    class Meta:
        model = Participation
        fields = '__all__'

class ParticipationSerializer(serializers.ModelSerializer):
    #student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    #degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())
    note = serializers.PrimaryKeyRelatedField(queryset=Notes.objects.all())
    class Meta:
        model = Participation
        fields = '__all__'
        
class TareaUrlSerializer(serializers.Serializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    
    class Meta:
        model = TareaUrl
        fields = '__all__'
        
class NotesSerializer(serializers.ModelSerializer):
    quetar = serializers.PrimaryKeyRelatedField(queryset=Quetar.objects.all())
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())

    class Meta:
        model = Notes
        fields = '__all__'
