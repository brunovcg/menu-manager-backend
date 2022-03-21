from django.urls import path
from .views import LoginView, SignupView, UserDetailView, ResetPasswordView, ChangePasswordView, UserView, MassiveLoadView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('users/', UserView.as_view()),
    path('users/<int:user_id>/', UserDetailView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/<int:user_id>/', ChangePasswordView.as_view()),
    path('massive-load/<int:user_id>/', MassiveLoadView.as_view()),

]
