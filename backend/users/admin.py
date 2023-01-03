from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': [('email', 'first_name'), ('username', 'last_name')]
        }),
        ('Права доступа', {
            'classes': ('collapse',),
            'fields': [('is_staff', 'is_superuser')],
        }),
    )
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    list_display_links = ('id', 'email', 'username')
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')


admin.site.register(Subscription)
