from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuetarViewSet,NotesViewSet,TareaUrlViewSet
from .models import Quetar,TareaUrl,Notes

pageName = {
    Quetar:'Trimestre',
    #FollowUp:'TrimestreDelEsudiante',
    TareaUrl:'Tarea',
    Notes:'Notas'
}

router=DefaultRouter()
router.register(pageName[Quetar],QuetarViewSet)
#router.register(pageName[FollowUp], FollowUpViewSet, basename='followup')
router.register(pageName[TareaUrl],TareaUrlViewSet, basename='Tareas')
router.register(pageName[Notes],NotesViewSet)


urlpatterns = [
    path('',include(router.urls)),
]
