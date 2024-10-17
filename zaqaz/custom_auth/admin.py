from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'name', 'email', 'phone', 'is_staff')
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone', 'password', 'is_staff')}),
    )

    # Если хотите добавить пользователей, нужно определить add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'phone', 'password1', 'password2', 'is_staff')}
        ),
    )

    list_filter = ('is_staff',)
    filter_horizontal = ()
