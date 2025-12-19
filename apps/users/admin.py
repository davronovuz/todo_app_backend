from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserAddress

class UserAddressInline(admin.StackedInline):
    model = UserAddress
    extra = 0
    can_delete = True

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_active', 'gender', 'created_at')
    search_fields = ('phone', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar', 'gender', 'date_of_birth')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    inlines = [UserAddressInline]

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'region', 'district', 'phone')
    search_fields = ('user__phone', 'region', 'district', 'street')
    list_filter = ('region',)