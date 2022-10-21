from django.shortcuts import render, redirect
# forms.py에서 가져오는 form
from .forms import CustomUserCreationForm
# 내장form에서 가져오는 form
from django.contrib.auth.forms import AuthenticationForm
# login인증 기능 모듈
from django.contrib.auth import login as auth_login
# Create your views here.
def index(request):
  return render(request, 'accounts/index.html')

def signup(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('accounts:index')
  else:
    form = CustomUserCreationForm
    context = {
      'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      auth_login(request, form.get_user())
      return redirect(request.GET.get('next') or 'accounts:index')
  else:
    form = AuthenticationForm
  context = {
    'form': form
  }
  return render(request, 'accounts/login.html', context)