# app/followups/permissions.py
from rest_framework.permissions import BasePermission
from .models import Teacher, TeacherSubject
from app.grades.models import GroupTeacher

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return Teacher.objects.filter(user=request.user).exists()
    
class IsTeacherCouser(BasePermission):
    def has_permission(self, request, view):
        teacher = Teacher.objects.filter(user=request.user).first()
        if not teacher:
            return False
        grade = request.data.get('grade_id')
        if not grade:
            return False

        teacherSubject = TeacherSubject.objects.filter(teacher=teacher)
        
        return GroupTeacher.objects.filter(grade=grade,teacherSubject__in=teacherSubject).exists()
        




    