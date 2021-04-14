from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import Reistrationform


def register(request):
    if request.method=="POST":
        form=Reistrationform(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account was created for {username}!')
            return redirect ("login")

    else:
        form=Reistrationform()
    return render(request,"accounts/register.html",{"form":form})

