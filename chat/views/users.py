from django.shortcuts import redirect
from django.urls import reverse_lazy
from ..forms import CustomUserCreationForm 
from django.contrib.auth import login , logout , update_session_auth_hash
from ..models import UserProfile 
from django.views.generic import DetailView , DeleteView , UpdateView , CreateView
from django.contrib.auth.views import (
    LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,
    PasswordResetConfirmView,PasswordResetCompleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin

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



class SignUpView(CreateView):
    template_name = 'registration/sign_up.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_online = True
        user.save()
        login(self.request, user)
        return super().form_valid(form)

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

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)  
        return response

    def get_success_url(self):
        return reverse_lazy('profile-detail', kwargs={"user_id": self.request.user.id})