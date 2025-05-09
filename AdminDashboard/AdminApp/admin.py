from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role','is_staff', 'is_superuser')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles and Permissions', {'fields': ('role', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )


# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)



