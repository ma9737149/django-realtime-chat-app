from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  




urlpatterns = [
    path('login/' , views.RedirectAuthenticatedUserLoginView.as_view() , name="login" ),
    path('logout/' , auth_views.LogoutView.as_view() , name="logout" ),
    path('sign-up/' , views.sign_up , name="sign-up" ),
    path('' , views.index , name="index"),
]
