from django.contrib import admin
from .models import Subject, Block, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['creator', 'subject', 'title', 'description', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
