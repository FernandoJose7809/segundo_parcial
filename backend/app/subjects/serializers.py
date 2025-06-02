from rest_framework import serializers
from app.subjects.models import *

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields='__all__'