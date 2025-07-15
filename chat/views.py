from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm 
from django.contrib.auth import login , logout
from .models import UserProfile , Room 
from django.views.generic import DetailView , DeleteView , UpdateView
from django.contrib.auth.views import (
    LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,
    PasswordResetConfirmView,PasswordResetCompleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class RedirectAuthenticatedUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)



class CustomLoginView(RedirectAuthenticatedUserMixin, LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        
        user = self.request.user
        user.is_online = True
        user.save()


        return response

class CustomPasswordResetView(RedirectAuthenticatedUserMixin, PasswordResetView):
    pass

class CustomPasswordResetDoneView(RedirectAuthenticatedUserMixin, PasswordResetDoneView):
    pass

class CustomPasswordResetConfirmView(RedirectAuthenticatedUserMixin, PasswordResetConfirmView):
    pass

class CustomPasswordResetCompleteView(RedirectAuthenticatedUserMixin, PasswordResetCompleteView):
    pass

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            user.is_online = False
            user.save()

        return super().dispatch(request, *args, **kwargs)



def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_online = True
        user.save()
        login(request, user)
        return redirect('index')

    return render(request, 'registration/sign_up.html', {'form': form})


class UserProfileDetailView(LoginRequiredMixin , DetailView):
    model = UserProfile
    template_name = "registration/user_profile.html"
    pk_url_kwarg = "user_id"

class UserDeleteView(LoginRequiredMixin , DeleteView):
    model = UserProfile
    template_name = 'registration/user_delete_confirm.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None) :
        return self.request.user


    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['username', 'email', 'profile']  
    template_name = 'registration/user_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self)  :
        return reverse_lazy('profile-detail' ,  kwargs =  { "user_id" : self.request.user.id })



class RoomDetailView(LoginRequiredMixin , DetailView):
    model = Room
    template_name = "rooms/room.html"
    pk_url_kwarg = "room_id"







@login_required
def index(request):
    return render(request , 'index.html')