from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, Report
from .forms import ReportForm, UserForm


class CustomUserAdmin(UserAdmin):
    form = UserForm
    list_display = ('username', 'email', 'role', 'manager', 'is_staff', 'is_superuser')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles and Permissions', {'fields': ('role', 'manager', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'manager','is_staff', 'is_superuser'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Allow superusers to see all users
        if request.user.is_superuser:
            return qs
        # Allow managers to see their own profile and assigned staff
        if request.user.role == 'manager':
            # Include the manager's own profile and their assigned staff
            return qs.filter(manager=request.user) | qs.filter(pk=request.user.pk)
        # Regular users should only see their own profile
        return qs.filter(pk=request.user.pk)


    def has_module_permission(self, request):
            if not request.user.is_authenticated:
                return False
            # Allow managers and admins to access the admin panel
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True  # Can view list
        # Managers can view their staff's profiles
        if request.user.role == 'MANAGER':
            return obj.manager == request.user or obj == request.user
        # Staff can only view their own profile
        return obj == request.user


    def has_change_permission(self, request, obj=None):
            # Allow managers to edit their profile and assigned staff members
            
            if request.user.role == 'manager':
                return obj is None or obj.manager == request.user
            
            return obj == request.user

    def has_delete_permission(self, request, obj=None):
            # Managers should not delete users, only admins
            if request.user.is_superuser:
                return True

class ReportAdmin(admin.ModelAdmin):
    form = ReportForm
    list_display = ('title', 'status', 'creator', 'submission_date', 'approval_date')
    list_filter = ('status', 'creator')
    search_fields = ('title', 'description', 'creator__username')
    ordering = ('-submission_date',)
    
   # Allow managers and staff to view their own and assigned reports
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Superusers see everything
        if request.user.is_superuser:
            return qs
        
        # Managers can see all reports
        if request.user.role == 'manager':
            return qs.filter(creator__manager=request.user)
        
        # Staff can only see their own reports
        return qs.filter(creator=request.user)
    
    def has_module_permission(self, request):
         return request.user.is_authenticated

    # Allow all roles to view reports
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if request.user.role == 'manager':
            return obj.creator.manager == request.user 
        return obj.creator == request.user

    # Allow all roles to add reports
    def has_add_permission(self, request):
        return request.user.role == 'staff'

    # Allow managers to add comments and staff to edit their own reports
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        # Managers can only add comments, not edit other fields
        if request.user.role == 'manager':
            return obj.creator.manager == request.user
        
        # Staff can only edit their own reports
        return obj is None or obj.creator == request.user or obj.status != 'approved'
    

    # Only superusers can delete reports
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # Limit fields based on roles
    def get_readonly_fields(self, request, obj=None):
        if request.user.role == 'manager':
            # Managers cannot edit these fields, only add comments
            return ['title', 'description', 'creator', 'submission_date', 'approval_date']
        return ['creator', 'submission_date','approval_date', 'status','manager_comment']
        
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user 
        super().save_model(request, obj, form, change)
    
    



# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Report, ReportAdmin)




