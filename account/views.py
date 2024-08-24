from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import LoginForm, UserRegistrationForm
from .models import Profile
from .forms import UserEditForm, ProfileEditForm


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


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, 'Registrations successfull')
            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            messages.error(request, 'Error updating your profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required()
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile edited succesfully')
            return HttpResponseRedirect(reverse_lazy('account:dashboard'))
        else:
            messages.error(request, 'Error editing you profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )
