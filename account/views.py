from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy

from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authentcated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Ivalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('account:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('account:password_reset_confirm')

    def get_success_url(self):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        return reverse_lazy('account:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
