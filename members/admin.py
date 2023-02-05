from django.contrib import admin
from members.models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        model = CustomUser
    list_display = ['username', 'email', 'is_active', 'is_staff']