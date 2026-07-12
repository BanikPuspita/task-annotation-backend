from django.contrib import admin
from .models import Image, Task, Annotation

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'uploaded_at']
    search_fields = ['title', 'user__username']
    list_filter = ['uploaded_at']
    readonly_fields = ['image_url', 'public_id']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'status', 'priority', 'task_date']
    search_fields = ['title', 'user__username']
    list_filter = ['status', 'priority', 'task_date']

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'label', 'created_at']
    search_fields = ['label', 'image__title']
    list_filter = ['created_at']