from django.shortcuts import render , redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.views import (
    LoginView,PasswordResetView,PasswordResetDoneView,
    PasswordResetConfirmView,PasswordResetCompleteView
)
from django.contrib.auth.decorators import login_required

class RedirectAuthenticatedUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)



class CustomLoginView(RedirectAuthenticatedUserMixin, LoginView):
    pass

class CustomPasswordResetView(RedirectAuthenticatedUserMixin, PasswordResetView):
    pass

class CustomPasswordResetDoneView(RedirectAuthenticatedUserMixin, PasswordResetDoneView):
    pass

class CustomPasswordResetConfirmView(RedirectAuthenticatedUserMixin, PasswordResetConfirmView):
    pass

class CustomPasswordResetCompleteView(RedirectAuthenticatedUserMixin, PasswordResetCompleteView):
    pass





def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('index')

    return render(request, 'registration/sign_up.html', {'form': form})


@login_required()
def index(request):
    return render(request , 'index.html')