from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from dashboard.choices import ActionChoices
from vault.models import PasswordEntry

from collections import Counter

UserModel = get_user_model()


class SecurityAudit(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='audits')

    total_passwords = models.IntegerField(default=0)
    weak_passwords = models.IntegerField(default=0)
    duplicate_passwords = models.IntegerField(default=0)
    old_passwords = models.IntegerField(default=0)

    security_score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Audit for {self.user.profile.username or self.user.email} - {self.created_at.strftime('%Y-%m-%d')}"

    def perform_audit(self):
        passwords = PasswordEntry.objects.filter(user=self.user)

        self.total_passwords = passwords.count()
        self.weak_passwords = passwords.filter(is_weak=True).count()

        password_values = passwords.values_list('password', flat=True)
        password_counts = Counter(password_values)
        self.duplicate_passwords = sum(count for count in password_counts.values() if count > 1)

        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        self.old_passwords = passwords.filter(updated_at__lt=six_months_ago).count()

        if self.total_passwords == 0:
            self.security_score = 0
        else:
            weak_penalty = (self.weak_passwords / self.total_passwords) * 40
            duplicate_penalty = (self.duplicate_passwords / self.total_passwords) * 30
            old_penalty = (self.old_passwords / self.total_passwords) * 30

            self.security_score = max(0, 100 - weak_penalty - duplicate_penalty - old_penalty)

        self.save()

        self.user.profile.security_score = int(self.security_score)
        self.user.profile.last_audit_date = self.created_at
        self.user.profile.save()


class AuditLog(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ActionChoices.choices)
    details = models.CharField(max_length=200, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.profil.username or self.user.email} - {self.get_action_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
