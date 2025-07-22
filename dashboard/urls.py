from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('audit/', views.SecurityAuditView.as_view(), name='security-audit'),
    path('history/', views.AuditHistoryView.as_view(), name='audit-history'),
    path('activity/', views.RecentActivityView.as_view(), name='recent-activity'),
    path('audit/run/', views.run_security_audit, name='run-security-audit'),
]