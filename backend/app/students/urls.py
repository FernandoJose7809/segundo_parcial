from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, TutorViewSet
from .models import Student,Tutor

pageName = {
    Student:'Estudiantes',
    Tutor:'Tutor'
}

router=DefaultRouter()
router.register(pageName[Student],StudentViewSet)
router.register(pageName[Tutor],TutorViewSet)
urlpatterns = [
    path('',include(router.urls)),
]