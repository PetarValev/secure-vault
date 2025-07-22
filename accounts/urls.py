from django.urls import path, include
from accounts import views

urlpatterns = [
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('', views.ProfileView.as_view(), name='profile'),
        path('edit/', views.profile_edit, name='profile-edit'),
        path('delete/', views.DeleteAccountView.as_view(), name='profile-delete'),
    ])),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change-password'),

]
