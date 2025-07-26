from django.contrib import admin
from django.utils.html import format_html
from vault.models import Category, PasswordEntry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_display', 'color_display', 'password_count']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 15

    fieldsets = (  # 5
        ('Category Info', {'fields': ('name',)}),
        ('Display', {'fields': ('icon', 'color')}),
    )

    actions = ['duplicate_categories']

    def icon_display(self, obj):
        return format_html('<i class="bi bi-{}"></i> {}', obj.icon, obj.icon)

    icon_display.short_description = 'Icon'

    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; color: white; border-radius: 3px;">{}</span>',
            obj.color, obj.color
        )

    color_display.short_description = 'Color'

    def password_count(self, obj):
        return obj.passwordentry_set.count()

    password_count.short_description = 'Passwords'

    def duplicate_categories(self, request, queryset):
        for category in queryset:
            category.pk = None
            category.name = f"{category.name} (Copy)"
            category.save()

    duplicate_categories.short_description = "Duplicate selected categories"


@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_email', 'username', 'category', 'strength_badge', 'is_weak', 'updated_at']
    list_filter = ['is_weak', 'category', 'created_at', 'updated_at']
    search_fields = ['title', 'username', 'email', 'user__email', 'website']
    ordering = ['-updated_at']
    readonly_fields = ['strength_score', 'is_weak', 'created_at', 'updated_at', 'last_used']
    list_per_page = 30
    date_hierarchy = 'created_at'

    fieldsets = (  # 8
        ('Basic Info', {'fields': ('user', 'category', 'title')}),
        ('Credentials', {'fields': ('username', 'email', 'password')}),
        ('Additional Info', {'fields': ('website', 'notes')}),
        ('Security', {'fields': ('strength_score', 'is_weak')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'last_used')}),
    )

    actions = ['mark_as_weak', 'mark_as_strong', 'update_strength']

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'

    def strength_badge(self, obj):
        if obj.strength_score >= 80:
            color = 'green'
            text = 'Strong'
        elif obj.strength_score >= 60:
            color = 'orange'
            text = 'Good'
        elif obj.strength_score >= 40:
            color = 'blue'
            text = 'Fair'
        else:
            color = 'red'
            text = 'Weak'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{} ({})</span>',
            color, text, obj.strength_score
        )

    strength_badge.short_description = 'Password Strength'
    strength_badge.admin_order_field = 'strength_score'

    def mark_as_weak(self, request, queryset):
        queryset.update(is_weak=True)

    mark_as_weak.short_description = "Mark selected passwords as weak"

    def mark_as_strong(self, request, queryset):
        queryset.update(is_weak=False)

    mark_as_strong.short_description = "Mark selected passwords as strong"

    def update_strength(self, request, queryset):
        for password in queryset:
            password.check_password_strength()
            password.save()

    update_strength.short_description = "Recalculate password strength"
