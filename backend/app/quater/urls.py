from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuetarViewSet,NotesViewSet,ExamViewSet,ParticipationViewSet,TaskViewSet,AttendanceViewSet
from .models import Quetar,Notes,Task,Participation,Attendance,Exam

pageName = {
    Quetar:'Trimestre',
    Attendance:'Asitencia',
    Task:'Tarea',
    Notes:'Notas',
    Participation:'Participacion',
    Exam:'Examenes'
}

router=DefaultRouter()
router.register(pageName[Quetar],QuetarViewSet)
router.register(pageName[Task], TaskViewSet, basename='Tareas')
router.register(pageName[Attendance],AttendanceViewSet, basename='Asistencia')
router.register(pageName[Exam],ExamViewSet, basename='Examenes')
router.register(pageName[Participation],ParticipationViewSet, basename='Participacion')
router.register(pageName[Notes],NotesViewSet)


urlpatterns = [
    path('',include(router.urls)),
]
