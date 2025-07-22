from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from vault.models import PasswordEntry
from dashboard.models import SecurityAudit, AuditLog
from dashboard.choices import ActionChoices
from core.utils import get_client_ip, get_user_agent
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def dashboard_view(request):
    user = request.user

    passwords = PasswordEntry.objects.filter(user=user)
    total_passwords = passwords.count()
    weak_passwords = passwords.filter(is_weak=True).count()

    latest_audit = SecurityAudit.objects.filter(user=user).first()

    recent_activity = AuditLog.objects.filter(user=user)[:5]

    if latest_audit:
        security_score = latest_audit.security_score
        last_audit_date = latest_audit.created_at
    else:
        security_score = 0
        last_audit_date = None

    recommendations = []
    if weak_passwords > 0:
        recommendations.append(f"You have {weak_passwords} weak passwords that need attention")
    if total_passwords == 0:
        recommendations.append("Start securing your accounts by adding your first password")
    if not last_audit_date:
        recommendations.append("Run your first security audit to see how secure you are")
    elif (timezone.now() - last_audit_date).days > 30:
        recommendations.append("It's been over 30 days since your last security audit")

    context = {
        'total_passwords': total_passwords,
        'weak_passwords': weak_passwords,
        'security_score': security_score,
        'last_audit_date': last_audit_date,
        'recent_activity': recent_activity,
        'recommendations': recommendations,
        'user_profile': user.userprofile,
    }


    return render(request, 'dashboard/dashboard.html', context)


class SecurityAuditView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/security-audit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update({
            'audit_history': SecurityAudit.objects.filter(user=user).order_by('-created_at')[:5],
            'has_passwords': PasswordEntry.objects.filter(user=user).exists(),
        })
        return context


class AuditHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/audit-history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        all_audits = SecurityAudit.objects.filter(user=user).order_by('-created_at')

        paginator = Paginator(all_audits, 7)
        page_number = self.request.GET.get('page')
        audits = paginator.get_page(page_number)

        context.update({
            'audits': audits,
            'all_audits': all_audits,
        })
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return super().get(request, *args, **kwargs)


class RecentActivityView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/recent-activity.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        all_logs = AuditLog.objects.filter(user=user).order_by('-timestamp')

        paginator = Paginator(all_logs, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            activity_logs = paginator.page(page_number)
        except PageNotAnInteger:
            activity_logs = paginator.page(1)
        except EmptyPage:
            activity_logs = paginator.page(paginator.num_pages)

        context.update({
            'activity_logs': activity_logs,
        })
        return context


@login_required
def run_security_audit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        user = request.user
        passwords = PasswordEntry.objects.filter(user=user)

        if not passwords.exists():
            return JsonResponse({
                'error': 'No passwords found to audit'
            }, status=400)

        audit = SecurityAudit.objects.create(user=user)
        audit.perform_audit()

        password_analysis = []
        for password in passwords:
            analysis = {
                'entry': {
                    'id': password.id,
                    'title': password.title,
                    'username': password.username or password.email or '-',
                    'strength_score': password.strength_score,
                    'updated_at': password.updated_at,
                },
                'issues': []
            }

            if password.is_weak:
                analysis['issues'].append('Weak password')
            if password.password in [p.password for p in passwords if p.id != password.id]:
                analysis['issues'].append('Duplicate password')
            if (timezone.now() - password.updated_at).days > 90:
                analysis['issues'].append('Password is old (90+ days)')

            password_analysis.append(analysis)

        AuditLog.objects.create(
            user=user,
            action=ActionChoices.AUDIT,
            details="Performed security audit",
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)
        )

        user.userprofile.security_score = audit.security_score
        user.userprofile.last_audit_date = audit.created_at
        user.userprofile.save()

        return JsonResponse({
            'success': True,
            'audit': {
                'id': audit.id,
                'security_score': audit.security_score,
                'total_passwords': audit.total_passwords,
                'weak_passwords': audit.weak_passwords,
                'duplicate_passwords': audit.duplicate_passwords,
                'old_passwords': audit.old_passwords,
                'created_at': audit.created_at.strftime('%B %d, %Y at %I:%M %p'),
            },
            'password_analysis': password_analysis,
            'message': 'Security audit completed successfully!'
        })

    except Exception as e:
        return JsonResponse({
            'error': f'Audit failed: {str(e)}'
        }, status=500)