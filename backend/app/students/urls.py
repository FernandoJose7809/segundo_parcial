from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet
from .models import Student

pageName = {
    Student:'Cursos',
}

router=DefaultRouter()
router.register(pageName[Student],StudentViewSet)
urlpatterns = [
    path('',include(router.urls)),
]