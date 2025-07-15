from django.conf import settings

from accounts.models import UserProfile


def app_context(request):
    return {
        'APP_NAME': 'SecureVault',
        'APP_VERSION': '1.0.0',
        'DEBUG': settings.DEBUG,
    }


def user_context(request):
    context = {}

    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            context.update({
                'user_security_score': profile.security_score,
                'user_has_profile': True,
            })

        except UserProfile.DoesNotExist:
            context['user_has_profile'] = False

    return context
