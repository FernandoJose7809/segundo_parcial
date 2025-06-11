from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradeViewSet, StudentCourseViewSet, DegreeSubjectViewSet, GroupTeacherViewSet
from .models import Grade, StudentCourse, DegreeSubject, GroupTeacher

pageName = {
    Grade:'Cursos',
    StudentCourse:'CursoPorEstudiante',
    DegreeSubject:'MateriaPorCurso',
    GroupTeacher:'CursoProfesor',
}

router=DefaultRouter()
router.register(pageName[Grade],GradeViewSet)
router.register(pageName[StudentCourse],StudentCourseViewSet)
router.register(pageName[DegreeSubject],DegreeSubjectViewSet)
router.register(pageName[GroupTeacher],GroupTeacherViewSet)


urlpatterns = [
    path('',include(router.urls)),
]
