from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Assuming your custom user model is named CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'city', 'state', 'address', 'phone', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)