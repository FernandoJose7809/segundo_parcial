from django.urls import path
from .views import PrediccionView

urlpatterns = [
    path('prediccion/', PrediccionView.as_view(), name='prediccion'),
]
