from django.urls import path, include
from vault import views

urlpatterns = [
    path('', views.VaultListView.as_view(), name='vault'),
    path('add/', views.PasswordCreateView.as_view(), name='add-password'),
    path('generator/', views.PasswordGeneratorView.as_view(), name='password-generator'),
    path('<int:pk>/', include([
        path('', views.PasswordDetailView.as_view(), name='password-detail'),
        path('edit/', views.PasswordUpdateView.as_view(), name='password-edit'),
        path('delete/', views.PasswordDeleteView.as_view(), name='password-delete'),
    ])),
]

