from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradeViewSet, StudentCourseViewSet, DegreeSubjectViewSet
from .models import Grade, StudentCourse, DegreeSubject

pageName = {
    Grade:'Cursos',
    StudentCourse:'CursoPorEstudiante',
    DegreeSubject:'MateriaPorCurso'
}

router=DefaultRouter()
router.register(pageName[Grade],GradeViewSet)
router.register(pageName[StudentCourse],StudentCourseViewSet)
router.register(pageName[DegreeSubject],DegreeSubjectViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
