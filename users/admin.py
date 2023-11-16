from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'username')
    list_display_links = ('id', 'name', 'email', 'username')
    search_fields = ('name', 'email', 'username')
    list_filter = ('name', 'email', 'username')
    readonly_fields = ('id',)


admin.site.register(User, UserAdmin)
