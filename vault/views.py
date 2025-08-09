from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from vault.models import PasswordEntry, Category
from vault.forms import PasswordEntryForm
from dashboard.models import AuditLog
from dashboard.choices import ActionChoices
from core.utils import get_client_ip, get_user_agent


class VaultListView(LoginRequiredMixin, ListView):
    model = PasswordEntry
    template_name = 'vault/vault.html'
    context_object_name = 'passwords'
    paginate_by = 6

    def get_queryset(self):
        queryset = PasswordEntry.objects.filter(user=self.request.user)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        sort = self.request.GET.get('sort', '-updated_at')
        if sort in ['title', '-title', 'updated_at', '-updated_at', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['total_passwords'] = self.get_queryset().count()
        context['weak_passwords'] = self.get_queryset().filter(is_weak=True).count()
        return context


class PasswordDetailView(LoginRequiredMixin, DetailView):
    model = PasswordEntry
    template_name = 'vault/password-detail.html'
    context_object_name = 'password'

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user)


class PasswordCreateView(LoginRequiredMixin, CreateView):
    model = PasswordEntry
    form_class = PasswordEntryForm
    template_name = 'vault/password-add.html'
    success_url = reverse_lazy('vault')

    def form_valid(self, form):
        form.instance.user = self.request.user

        AuditLog.objects.create(
            user=self.request.user,
            action=ActionChoices.CREATE,
            details=f"Added password for {form.instance.title}",
            ip_address=get_client_ip(self.request),
            user_agent=get_user_agent(self.request)
        )

        messages.success(self.request, f'Password for {form.instance.title} has been saved securely!')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    model = PasswordEntry
    form_class = PasswordEntryForm
    template_name = 'vault/password-edit.html'
    success_url = reverse_lazy('vault')

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        AuditLog.objects.create(
            user=self.request.user,
            action=ActionChoices.UPDATE,
            details=f"Updated password for {form.instance.title}",
            ip_address=get_client_ip(self.request),
            user_agent=get_user_agent(self.request)
        )

        messages.success(self.request, f'Password for {form.instance.title} has been updated!')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PasswordDeleteView(LoginRequiredMixin, DeleteView):
    model = PasswordEntry
    template_name = 'vault/password-delete.html'
    success_url = reverse_lazy('vault')
    context_object_name = 'password'

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = self.get_object()
        title = self.object.title

        try:
            log = AuditLog.objects.create(
                user=self.request.user,
                action=ActionChoices.DELETE,
                details=f"Deleted password for {title}",
                ip_address=get_client_ip(self.request),
                user_agent=get_user_agent(self.request),
            )
            print(f"Log created: {log.pk}")
        except Exception as e:
            print(f"Error creating log: {e}")

        messages.success(self.request, f'Password for {title} has been deleted.')

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PasswordGeneratorView(LoginRequiredMixin, TemplateView):
    template_name = 'vault/password-generator.html'
