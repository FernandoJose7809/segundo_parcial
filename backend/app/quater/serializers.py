from rest_framework import serializers
from .models import Quetar, Notes, Task, Attendance, Exam,Participation #,FollowUp
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
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all(), write_only=True)
    note = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Attendance
        fields = ['id','its_here', 'date', 'degreeSubject', 'note']

class TaskSerializer(serializers.ModelSerializer):
    #student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all(), write_only=True)
    note = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Task
        fields = ['id','value', 'start_date', 'end_date', 'degreeSubject', 'note','url']

class ExamSerializer(serializers.ModelSerializer):
    #student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all(), write_only=True)    
    note = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Exam
        fields = ['id','value', 'degreeSubject', 'note', 'date']

class ParticipationSerializer(serializers.ModelSerializer):
    # degreeSubject no está declarado explícitamente
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all(), write_only=True)  # <-- agregar esto
    note = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Participation
        fields = ['id','value', 'degreeSubject', 'note']

# class TareaUrlSerializer(serializers.Serializer):
#     task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    
#     class Meta:
#         model = TareaUrl
#         fields = '__all__'
        
class NotesSerializer(serializers.ModelSerializer):
    quetar = serializers.PrimaryKeyRelatedField(queryset=Quetar.objects.all())
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())

    class Meta:
        model = Notes
        fields = '__all__'
