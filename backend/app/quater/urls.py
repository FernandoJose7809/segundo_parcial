from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuetarViewSet,FollowUpViewSet
from .models import Quetar,FollowUp

pageName = {
    Quetar:'Trimestre',
    FollowUp:'TrimestreDelEsudiante',
}

router=DefaultRouter()
router.register(pageName[Quetar],QuetarViewSet)
router.register(pageName[FollowUp],FollowUpViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
