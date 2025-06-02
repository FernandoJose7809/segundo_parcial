from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet,TeacherSubjectViewSet
from .models import Teacher,TeacherSubject

pageName = {
    Teacher:'Profesores',
    TeacherSubject:'MateriaPorProfesor'
}

router=DefaultRouter()
router.register(pageName[Teacher],TeacherViewSet)
router.register(pageName[TeacherSubject],TeacherSubjectViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
