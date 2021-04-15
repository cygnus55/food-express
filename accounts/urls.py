from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views 
from django.urls import reverse_lazy


app_name = 'accounts'


urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name="accounts/login.html"),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name="accounts/logout.html"),name="logout"),
    path('register/',views.register,name='register'),
    path('password_change/',
                auth_views.PasswordChangeView.as_view(template_name="accounts/password_change_form.html",success_url=reverse_lazy('accounts:password_change_done')),name='password_change'),
    path('password_change/done/',
                    auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"),name='password_change_done'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html',
             success_url=reverse_lazy('accounts:password_reset_done'),
             email_template_name='accounts/password_reset_email.html',
        ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete'),
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html',
            
              ),
         name='password_reset_complete'),
                    
]
