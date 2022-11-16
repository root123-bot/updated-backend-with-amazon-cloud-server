from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'joined')
    date_hierarchy = 'joined'
    list_filter = ('joined',    )
    search_fields = ('email',)

    fieldsets = (
        (None, {
            'fields': (
                'email', 'password'
            ),
        }),
        ('User status', {
            'fields': (
                'is_staff', 'is_superuser', 'is_active'
            ),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)