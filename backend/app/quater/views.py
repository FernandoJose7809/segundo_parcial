from django.shortcuts import render
from rest_framework import viewsets
from .models import Quetar,FollowUp
from .serializers import QuetarSerializer,FollowUpSerializer
# Create your views here.

class QuetarViewSet(viewsets.ModelViewSet):
    queryset = Quetar.objects.all()
    serializer_class = QuetarSerializer

class FollowUpViewSet(viewsets.ModelViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer