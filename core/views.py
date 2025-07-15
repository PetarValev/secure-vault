from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from accounts.models import UserProfile


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    context = {
        'total_users': UserProfile.objects.count(),
        'app_name': 'SecureVault',
        'features': [
            {
                'icon': 'shield-check',
                'title': 'Secure Storage',
                'description': 'Your passwords are encrypted and stored securely'
            },
            {
                'icon': 'speedometer2',
                'title': 'Security Audit',
                'description': 'Regular audits help you maintain strong passwords'
            },
            {
                'icon': 'people',
                'title': 'User Friendly',
                'description': 'Simple and intuitive interface for everyone'
            }
        ]
    }
    return render(request, 'core/home.html', context)


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app_name': 'SecureVault',
            'version': '1.0.0',
            'security_tips': [
                'Use unique passwords for each account',
                'Enable two-factor authentication when possible',
                'Regularly update your passwords',
                'Avoid using personal information in passwords',
                'Use a password manager (like this one!)'
            ]
        })
        return context