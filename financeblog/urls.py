"""financeblog URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from account import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('questions/', include('advice.urls', namespace='advice')),

    path('register/', account_views.register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(template_name="account/login.html"),
         name="login"),
    path('logout/',
         auth_views.LogoutView.as_view(template_name="account/logout.html"),
         name="logout"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name="account/password_reset.html"),
         name="password_reset"),
    path('password-reset/confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(
             template_name="account/password_reset_done.html"),
         name="password_reset_done"),
    path('password-reset/complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/password_reset_complete.html"),
         name="password_reset_complete"),

    path('profile/update', account_views.update_profile, name="update"),
    path('profile/<int:pk>', account_views.profile, name="profile"),
    path('', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
