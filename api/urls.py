from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    login,
    profile,
    TaskListCreateView,
    TaskDetailView,
    ImageListCreateView,
    AnnotationListCreateView,
    AnnotationDetailView,
)


urlpatterns = [
    path("login/", login),
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