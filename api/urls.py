from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import profile, TaskListCreateView,TaskDetailView, ImageListCreateView, AnnotationListCreateView, AnnotationDetailView


urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("profile/", profile),
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/",TaskDetailView.as_view(),
    name="task-detail"),
    path("images/",ImageListCreateView.as_view(),
    name="image-list-create"),
    path(
    "annotations/",
    AnnotationListCreateView.as_view(),
    name="annotation-list-create",
),

path(
    "annotations/<int:pk>/",
    AnnotationDetailView.as_view(),
    name="annotation-detail",
),
]