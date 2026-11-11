from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("reset-progress/", views.reset_progress, name="reset_progress"),
    path("paths/", views.path_index, name="path_index"),
    path("paths/<slug:slug>/", views.path_detail, name="path_detail"),
    path("lessons/<slug:slug>/", views.lesson_detail, name="lesson_detail"),
]
