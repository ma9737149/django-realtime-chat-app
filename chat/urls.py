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

    path('change_password/' , auth_views.PasswordChangeView.as_view() , name='change_password'),
    path('change_password_done/' , auth_views.PasswordChangeDoneView.as_view() , name='password_change_done'),

    path('user/<int:user_id>' , views.UserProfileDetailView.as_view() , name="profile-detail"),
    path('user/delete' , views.UserDeleteView.as_view() , name="user-delete"),
    path('user/update' , views.UserUpdateView.as_view() , name="user-update"),
    
    path('room/<int:room_id>' , views.RoomDetailView.as_view() , name="room-detail")
]
