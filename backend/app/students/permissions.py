from rest_framework.permissions import BasePermission
from .models import Student

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return Student.objects.filter(user=request.user).exists