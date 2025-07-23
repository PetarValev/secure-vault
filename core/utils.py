import secrets
import string
import re

from django.contrib.auth import get_user_model

UserModel = get_user_model()

def get_user_stats():
    return {
        'total_users': UserModel.objects.filter(is_active=True).count(),
        'total_profiles': UserModel.objects.filter(
            profile__isnull=False
        ).count(),
    }


def calculate_password_strength(password):
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

    return min(score, 100)


def get_password_strength_label(score):
    if score >= 80:
        return "Strong", "success"
    elif score >= 60:
        return "Good", "warning"
    elif score >= 40:
        return "Fair", "info"
    else:
        return "Weak", "danger"


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', 'Unknown')[:200]


def is_password_common(password):
    common_passwords = [
        'password', '123456', '123456789', 'qwerty', 'abc123',
        'password123', 'admin', 'letmein', 'welcome', 'monkey',
        '1234567890', 'password1', '123123', 'qwerty123'
    ]

    return password.lower() in common_passwords


def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:95] + ('.' + ext if ext else '')

    return filename