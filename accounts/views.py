from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .models import User 
from .forms import RegistrationForm, LoginForm 
from restaurants.forms import RestaurantProfileForm
from customer.forms import CustomerProfileForm
from .tokens import account_activation_token
from .tasks import activate_account_email_task


def user_login(request):
    if request.method == 'POST':
        next_url = request.GET.get('next')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                _user = User.objects.get(username__iexact=cd['username'])
                if not _user.is_active:
                    messages.error(request, 'Your account is not confirmed yet. Check your email.')
                    return redirect('accounts:login')
            except Exception:
                messages.error(request,'Username or password incorrect!')
                return redirect('accounts:login')

            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    if next_url:
                        return redirect(next_url)
                    if user.is_superuser and user.is_staff:
                        return redirect('admin:index')
                    elif user.is_customer:
                        return redirect('customer:homepage')
                    elif user.is_restaurant:
                        return redirect('restaurants:restaurant_dashboard')
                    elif user.is_delivery_person:
                        return redirect('delivery_person:home')
                messages.error(request, 'Your account is not confirmed yet. Check your email.')
                return redirect('accounts:login')
            else:
                messages.error(request,'Username or password incorrect!')
                return redirect('accounts:login')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def register(request,role):
    allowed_roles = ['customer', 'restaurant']

    if role not in allowed_roles:
        raise Http404()

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if role == 'restaurant':
            profile_form = RestaurantProfileForm(data=request.POST, files=request.FILES)
        else:
            profile_form = CustomerProfileForm(data=request.POST, files=request.FILES)
        print(form.errors.as_data())
        print(profile_form.errors.as_data())
        if form.is_valid() and profile_form.is_valid():
            new_user = form.save(commit=False)
            setattr(new_user, f'is_{role}', True)
            new_user.is_active = False
            new_user.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = new_user
            user_profile.save()
            current_site = get_current_site(request)
            message = render_to_string('accounts/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token':account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data['email']
            activate_account_email_task.delay(message, to_email)
            messages.error(request, 'Please confirm your email address to complete the registration.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Error in registrating!')
    else:
        form = RegistrationForm()
        if role == 'restaurant':
            profile_form = RestaurantProfileForm()
        else:
            profile_form = CustomerProfileForm()
    
    context = {
        'form': form,
        'profile_form': profile_form,
        'title': 'Register',
        'role': role.title()
    }

    return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('accounts:login')