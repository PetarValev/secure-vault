from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from accounts.models import AppUser, Profile


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    list_display = ['email', 'is_active', 'is_staff', 'is_superuser', 'last_login']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ['last_login']
    list_per_page = 25

    fieldsets = (
        ('Authentication', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_users.short_description = "Deactivate selected users"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'username', 'security_score_badge', 'last_audit_date', 'created_at']
    list_filter = ['created_at', 'last_audit_date']
    search_fields = ['user__email', 'username']
    ordering = ['-security_score']
    readonly_fields = ['created_at', 'weak_passwords_count']
    list_per_page = 20

    fieldsets = (
        ('Profile Info', {'fields': ('user', 'username')}),
        ('Security', {'fields': ('security_score', 'last_audit_date', 'weak_passwords_count')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def security_score_badge(self, obj):
        if obj.security_score >= 80:
            color = 'green'
        elif obj.security_score >= 60:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/100</span>',
            color, obj.security_score
        )

    security_score_badge.short_description = 'Security Score'
    security_score_badge.admin_order_field = 'security_score'