import json
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, ProfileUpdateForm
from core.utils import get_client_ip, get_user_agent
from dashboard.choices import ActionChoices
from dashboard.models import AuditLog


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        AuditLog.objects.create(
            user=self.request.user,
            action=ActionChoices.LOGIN,
            details="User logged in",
            ip_address=get_client_ip(self.request),
            user_agent=get_user_agent(self.request)
        )

        messages.success(self.request, f'Welcome {self.object.email}! Your account has been created.')
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_valid(self, form):
        AuditLog.objects.create(
            user=form.get_user(),
            action=ActionChoices.LOGIN,
            details="User logged in",
            ip_address=get_client_ip(self.request),
            user_agent=get_user_agent(self.request)
        )

        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            AuditLog.objects.create(
                user=request.user,
                action=ActionChoices.LOGOUT,
                details="User logged out",
                ip_address=get_client_ip(request),
                user_agent=get_user_agent(request)
            )

        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)

        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['user_profile'] = self.request.user.profile
        context['weak_passwords_count'] = self.request.user.profile.weak_passwords_count
        return context


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile-edit.html', context)


class DeleteAccountView(LoginRequiredMixin, View):
    template_name = 'accounts/delete_account.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})

    def post(self, request):
        try:
            data = json.loads(request.body)
            password = data.get('password')

            if not request.user.check_password(password):
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid password'
                })

            user_email = request.user.email
            request.user.delete()
            logout(request)

            return JsonResponse({
                'success': True,
                'message': f'Account {user_email} has been permanently deleted.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'Something went wrong. Please try again.'
            })


class CustomPasswordChangeView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            old_password = data.get('old_password')
            new_password1 = data.get('new_password1')
            new_password2 = data.get('new_password2')

            form_data = {
                'old_password': old_password,
                'new_password1': new_password1,
                'new_password2': new_password2
            }

            form = PasswordChangeForm(request.user, form_data)

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)

                AuditLog.objects.create(
                    user=request.user,
                    action='update',
                    details=f'Password changed for user {request.user.email}',
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                return JsonResponse({
                    'success': True,
                    'message': 'Password changed successfully!'
                })
            else:
                errors = []
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        errors.append(str(error))

                return JsonResponse({
                    'success': False,
                    'error': ' '.join(errors)
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'Something went wrong. Please try again.'
            })
