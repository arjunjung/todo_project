from django.contrib import admin
from .models import Todo


class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Todo,ToDoAdmin)
