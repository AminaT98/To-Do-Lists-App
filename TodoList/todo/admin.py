from django.contrib import admin
from .models import Task, List

# Register your models here.

admin.site.site_header = "To-Do App Administration"
admin.site.site_title = "To-Do App Admin Portal"
admin.site.index_title = "Welcome to the To-Do App Admin Area"

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'list')
    list_filter = ('completed', 'list')
    search_fields = ('title', 'description', 'list__name', 'list__date')
    ordering = ('list__date',)
    
    
@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name', 'date')
    ordering = ('-date',)