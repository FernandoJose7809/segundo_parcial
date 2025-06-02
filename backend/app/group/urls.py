from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet,GroupTeacherViewSet
from .models import Group,GroupTeacher

pageName={
    Group:'Gupos',
    GroupTeacher:'GrupoPorProfesor'
}

router=DefaultRouter()
router.register(pageName[Group],GroupViewSet)
router.register(pageName[GroupTeacher],GroupTeacherViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
