from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  




urlpatterns = [
    path('' , views.index , name="index"),

    path('login/' , views.CustomLoginView.as_view() , name="login" ),
    path('logout/' , views.CustomLogoutView.as_view() , name="logout" ),
    path('sign-up/' , views.sign_up , name="sign-up" ),

    path('reset_password/', views.CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', views.CustomPasswordResetView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_complete'),
]
