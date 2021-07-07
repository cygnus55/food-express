from django.shortcuts import render,redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm 
from restaurants.forms import RestaurantProfileForm
from customer.forms import CustomerProfileForm

def user_login(request):
    if request.method == 'POST':
        next_url = request.GET.get('next')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
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
                else:
                    messages.error(request, 'Your account has been disabled, as you remain deactive for long time.')
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
        if form.is_valid() and profile_form.is_valid():
            new_user = form.save(commit=False)
            setattr(new_user, f'is_{role}', True)
            new_user.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = new_user
            user_profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}!')
            return redirect('accounts:login')
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