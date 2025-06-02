from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet
from .models import Subject

pageName = {
    Subject:'Materias',
}

router=DefaultRouter()
router.register(pageName[Subject],SubjectViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
