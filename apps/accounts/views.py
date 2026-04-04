from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .permissions import requires_permission
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Will redirect to dashboard once dashboard app is connected
            return redirect('/') 
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@requires_permission('manage_users')
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

from apps.core.tenant import get_current_tenant

@requires_permission('manage_users')
def user_create(request):
    db_name = get_current_tenant() or 'default'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, using_db=db_name)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_list')
    else:
        form = CustomUserCreationForm(using_db=db_name)
    return render(request, 'accounts/user_form.html', {'form': form})
