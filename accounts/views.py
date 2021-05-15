from django.shortcuts import render,redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import Registrationform, LoginForm 
from restaurants.forms import RestaurantProfileForm
from customer.forms import CustomerProfileForm
from restaurants.models import Restaurant
from customer.models import Customer


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser and user.is_staff:
                        return redirect('admin:index')
                    elif user.is_customer:
                        return redirect('customer:homepage')
                    elif user.is_restaurant:
                        # return HttpResponseRedirect(reverse('restaurants:restaurant_dashboard', args=(user.username,)))
                        return redirect('restaurants:restaurant_dashboard', username=user.username)
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def register(request,role):
    allowed_roles = ['customer', 'restaurant']
    if role not in allowed_roles:
        raise Http404()
    if request.method=="POST":
        form=Registrationform(request.POST)
        if role == 'restaurant':
            profile_form = RestaurantProfileForm(request.POST)
        else:
            profile_form = CustomerProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            new_user = form.save(commit=False)
            setattr(new_user, f'is_{role}', True)
            new_user.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = new_user
            user_profile.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account was created for {username}!')
            return redirect ("accounts:login")

    else:
        form = Registrationform()
        if role == 'restaurant':
            profile_form = RestaurantProfileForm()
        else:
            profile_form = CustomerProfileForm()
    
    context = {
        'form': form,
        'profile_form': profile_form,
        'title': 'Register'
    }
    return render(request, "accounts/register.html", context)