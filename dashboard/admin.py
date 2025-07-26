from django.contrib import admin
from django.utils.html import format_html
from dashboard.models import SecurityAudit, AuditLog


@admin.register(SecurityAudit)
class SecurityAuditAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'security_score_badge', 'total_passwords', 'weak_passwords', 'duplicate_passwords',
                    'created_at']
    list_filter = ['created_at', 'security_score']
    search_fields = ['user__email', 'user__profile__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 25

    fieldsets = (
        ('Audit Info', {'fields': ('user', 'created_at')}),
        ('Results', {'fields': ('security_score', 'total_passwords')}),
        ('Issues Found', {'fields': ('weak_passwords', 'duplicate_passwords', 'old_passwords')}),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'

    def security_score_badge(self, obj):
        if obj.security_score >= 80:
            color = 'green'
            emoji = '😊'
        elif obj.security_score >= 60:
            color = 'orange'
            emoji = '😐'
        else:
            color = 'red'
            emoji = '😞'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {} {}/100</span>',
            color, emoji, obj.security_score, obj.security_score
        )

    security_score_badge.short_description = 'Security Score'
    security_score_badge.admin_order_field = 'security_score'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'action_badge', 'details_short', 'ip_address', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__email', 'details', 'ip_address']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    list_per_page = 50

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'

    def action_badge(self, obj):
        colors = {
            'login': 'green',
            'logout': 'blue',
            'create': 'purple',
            'update': 'orange',
            'delete': 'red',
            'audit': 'teal',
        }
        color = colors.get(obj.action, 'gray')

        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px;">{}</span>',
            color, obj.get_action_display()
        )

    action_badge.short_description = 'Action'
    action_badge.admin_order_field = 'action'

    def details_short(self, obj):
        return obj.details[:50] + ('...' if len(obj.details) > 50 else '')

    details_short.short_description = 'Details'
