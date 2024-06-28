from django.urls import path
from . import views



urlpatterns = [
    path("upload", views.file_upload),
    path('download/<str:file_path>/', views.download_file, name='download_file'),
    path("", views.home)
]