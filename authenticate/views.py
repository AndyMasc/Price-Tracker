from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, AuthorizeUser

# Create your views here.

@login_required
def account(request):
    return render(request, 'authenticate/account.html')

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('home:index')
    else:
        form = CreateUserForm()
        context = {'form':form}
    return render(request, 'authenticate/register.html', context)

def signin(request):
    form = AuthorizeUser(request)
    context = {'form': form}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:index')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'authenticate/signin.html', context)

@login_required()
def signout(request):
    logout(request)
    return redirect('home:index')

@login_required()
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, 'Your account has been deleted successfully.')
    return redirect('authenticate:signin')