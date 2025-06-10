from rest_framework import serializers
from .models import Quetar,FollowUp,TareaUrl, Notes
from app.students.models import Student
from app.grades.models import DegreeSubject

class QuetarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quetar
        fields = '__all__'


class FollowUpSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())
    note = serializers.PrimaryKeyRelatedField(queryset=Notes.objects.all())

    class Meta:
        model = FollowUp
        fields = '__all__'
        
class TareaUrlSerializer(serializers.Serializer):
    followUp= serializers.PrimaryKeyRelatedField(queryset=FollowUp.objects.all())
    
    class Meta:
        model = TareaUrl
        fields = '__all__'
        
class NotesSerializer(serializers.ModelSerializer):
    quetar = serializers.PrimaryKeyRelatedField(queryset=Quetar.objects.all())
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())

    class Meta:
        model = Notes
        fields = '__all__'
