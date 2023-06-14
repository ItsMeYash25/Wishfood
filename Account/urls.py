from django.urls import path
from .views import Login, Signup, Logout, change_password
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', Login, name="login"),
    path('signup', Signup, name="signup"),
    path('logout', Logout, name="logout"),
    path('change-password', change_password, name="change_password"),

    path("password_reset", auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="password_reset"),
    path("password_reset/done", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password_reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path("password_reset-complete", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),

]
