from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('profile/reserve-history/', views.ReserveHistoryView.as_view(), name="reserve_history"),
    path('profile/edit-profile/', views.EditProfileView.as_view(), name="edit_profile"),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name="change_password"),
]