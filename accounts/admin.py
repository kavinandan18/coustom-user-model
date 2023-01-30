from django.contrib import admin
from accounts.models import User,Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','location')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email','get_full_name',  'is_staff')
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    pass