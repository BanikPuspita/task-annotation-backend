from django.contrib import admin
from .models import Task, Image, Annotation


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "status",
        "priority",
        "due_date",
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "uploaded_at",
    )


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "created_at",
    )