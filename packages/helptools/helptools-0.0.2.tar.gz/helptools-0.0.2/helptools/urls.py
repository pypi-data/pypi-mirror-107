from django.urls import path
from . import views

urlpatterns = [
    path('', views.docs),
    path('files/<str:file_name>', views.file),
]