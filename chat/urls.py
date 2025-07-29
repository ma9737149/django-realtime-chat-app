from django.urls import path
from django.contrib.auth import views as users_views  
from .views import rooms , users


urlpatterns = [
    path('login/' , users.CustomLoginView.as_view() , name="login" ),
    path('logout/' , users.CustomLogoutView.as_view() , name="logout" ),
    path('sign-up/' , users.SignUpView.as_view() , name="sign-up" ),
    path('reset_password/', users.CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', users.CustomPasswordResetView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', users.CustomPasswordResetDoneView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', users.CustomPasswordResetConfirmView.as_view(), name='password_reset_complete'),
    path('change_password/' , users_views.PasswordChangeView.as_view() , name='change_password'),
    path('change_password_done/' , users_views.PasswordChangeDoneView.as_view() , name='password_change_done'),
    path('user/<int:user_id>' , users.UserProfileDetailView.as_view() , name="profile-detail"),
    path('user/delete' , users.UserDeleteView.as_view() , name="user-delete"),
    path('user/update' , users.UserUpdateView.as_view() , name="user-update"),


    path('' , rooms.RoomView.as_view() , name="index"),
    path('room/<int:room_id>' , rooms.RoomDetailView.as_view() , name="room-detail")
]
