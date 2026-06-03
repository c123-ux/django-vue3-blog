from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_public', 'updated_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['title', 'content', 'tags']
