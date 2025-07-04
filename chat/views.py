from django.http import HttpResponse
from django.shortcuts import render , redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.views import LoginView

class RedirectAuthenticatedUserLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index') 
        return super().dispatch(request, *args, **kwargs)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('index')

    return render(request, 'registration/sign_up.html', {'form': form})



def index(request):
    return HttpResponse(f'you are logged in as {request.user.username}')