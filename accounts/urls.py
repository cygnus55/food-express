from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from accounts import views

app_name = 'accounts'

urlpatterns = [
     path('login/', views.user_login, name='login'),
     path(
          'logout/', 
          auth_views.LogoutView.as_view(
               template_name='accounts/logout.html'
          ), 
          name='logout'
     ),
     path('register/<str:role>/', views.register, name='register'),
     path(
          'password-change/',
          auth_views.PasswordChangeView.as_view(
               template_name='accounts/password_change_form.html', 
               success_url=reverse_lazy('accounts:password_change_done')
          ), 
          name='password_change'
     ),
     path(
          'password-change/done/',
          auth_views.PasswordChangeDoneView.as_view(
               template_name='accounts/password_change_done.html'
          ), 
          name='password_change_done'
     ),
     path(
          'password-reset/',
          auth_views.PasswordResetView.as_view(
               template_name='accounts/password_reset_form.html',
               success_url=reverse_lazy('accounts:password_reset_done'),
               email_template_name='accounts/password_reset_email.html',
          ),
          name='password_reset'
     ),
     path(
          'password-reset/done/',
          auth_views.PasswordResetDoneView.as_view(
               template_name='accounts/password_reset_done.html',
          ),
          name='password_reset_done'
     ),
     path(
          'password-reset-confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(
               template_name='accounts/password_reset_confirm.html',
               success_url=reverse_lazy('accounts:password_reset_complete'),
          ),
          name='password_reset_confirm'
     ),
     path(
          'password-reset-complete/',
          auth_views.PasswordResetCompleteView.as_view(
               template_name='accounts/password_reset_complete.html'
          ),
          name='password_reset_complete'
     ), 
      path(
    'activate/<slug:uidb64>/<slug:token>/',
    views.activate, 
    name='activate'
),             
]
