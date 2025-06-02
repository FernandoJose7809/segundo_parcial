from rest_framework import serializers
from .models import *
from app.students.models import Student
from app.grades.models import DegreeSubject

class QuetarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quetar
        fields = '__all__'


class FollowUpSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    degreeSubject = serializers.PrimaryKeyRelatedField(queryset=DegreeSubject.objects.all())
    quetar = serializers.PrimaryKeyRelatedField(queryset=Quetar.objects.all())

    class Meta:
        model = FollowUp
        fields = '__all__'
