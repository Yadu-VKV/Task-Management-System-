from django.contrib import admin
from .models import User, Project, Task

# Register your models here.

# Customizing the User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )

# Customizing the Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'team_lead', 'created_by', 'created_at')
    list_filter = ('created_at', 'team_lead')
    search_fields = ('name', 'description', 'team_lead__username', 'created_by__username')
    ordering = ('created_at',)
    fields = ('name', 'description', 'team_lead', 'created_by', 'created_at')
    readonly_fields = ('created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Customizing the Task Admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'project')
    search_fields = ('title', 'description', 'assigned_to__username', 'project__name')
    ordering = ('created_at',)
    fields = ('title', 'description', 'project', 'assigned_to', 'status', 'created_at')
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
