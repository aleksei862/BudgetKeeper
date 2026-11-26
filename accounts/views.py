from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .decorators import role_required

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна.')
            return redirect('profile')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы вошли в систему.')
            return redirect('profile')
        else:
            messages.error(request, 'Неверные учётные данные.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')


import secrets
import hashlib
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import PasswordResetToken
from .forms import ForgotPasswordForm, ResetPasswordForm

User = get_user_model()


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                raw_token = secrets.token_urlsafe(32)
                hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

                # Инвалидация старых токенов
                PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)
                PasswordResetToken.objects.create(user=user, token_hash=hashed_token)

                reset_url = request.build_absolute_uri(reverse('reset_password', kwargs={'token': raw_token}))

                # Отправляем письмо
                send_mail(
                    'Восстановление пароля',
                    f'Для сброса пароля перейдите по ссылке: {reset_url}',
                    None,
                    [user.email],
                    fail_silently=False,
                )

            # Единый ответ для безопасности
            messages.success(request, 'Если аккаунт с таким email существует, письмо отправлено.')
            return redirect('login')
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_password_view(request, token):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    reset_token = PasswordResetToken.objects.filter(token_hash=hashed_token, is_used=False).first()

    if not reset_token or not reset_token.is_valid():
        messages.error(request, 'Ссылка недействительна или истек её срок действия.')
        return redirect('login')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = reset_token.user
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Инвалидация токена
            reset_token.is_used = True
            reset_token.save()

            messages.success(request, 'Пароль успешно изменён. Войдите с новым паролем.')
            return redirect('login')
    else:
        form = ResetPasswordForm()
    return render(request, 'accounts/reset_password.html', {'form': form})