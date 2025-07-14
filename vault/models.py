from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, default='key')
    color = models.CharField(max_length=7, default='#007bff')

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class PasswordEntry(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='passwords')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, help_text="e.g., Gmail, Facebook")
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=500)
    website = models.URLField(blank=True, help_text="e.g., https://gmail.com")
    notes = models.TextField(blank=True, max_length=500)

    is_weak = models.BooleanField(default=False)
    strength_score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Password Entries"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def check_password_strength(self):
        password = self.password
        score = 0

        if len(password) >= 8:
            score += 25
        if len(password) >= 12:
            score += 25
        if any(c.isupper() for c in password):
            score += 15
        if any(c.islower() for c in password):
            score += 15
        if any(c.isdigit() for c in password):
            score += 10
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            score += 10

        self.strength_score = min(score, 100)
        self.is_weak = score < 60

    def save(self, *args, **kwargs):
        self.check_password_strength()
        super().save(*args, **kwargs)
