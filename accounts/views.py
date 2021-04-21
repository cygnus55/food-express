from django.shortcuts import render,redirect, reverse
from django.contrib import messages
from .forms import Registrationform, LoginForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .decorators import customer_required
from .models import User


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_customer:
                        return HttpResponse('Customer logged in')
                    elif user.is_restaurant:
                        return HttpResponseRedirect(reverse('restaurants:restaurant_dashboard', args=(user.username,)))
                        # return redirect(f"'restaurants:restaurant_dashboard' '{user.username}'")
                    else:
                        return HttpResponse('Chef Logged in')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def register(request,role):
    allowed_roles = ['customer', 'restaurant', 'chef']
    if role not in allowed_roles:
        raise Http404()
    if request.method=="POST":
        form=Registrationform(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            setattr(new_user, f'is_{role}', True)
            new_user.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account was created for {username}!')
            return redirect ("accounts:login")

    else:
        form=Registrationform()
    return render(request,"accounts/register.html",{"form":form})


@login_required
@customer_required
def customer_homepage(request):
    return render(request, 'customer_homepage.html')