from django.urls import path
from .views import SignUpView, ProfileUpdate,EmailUpdate
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('signup', SignUpView.as_view(),name='signup'),
    path('profile/',login_required(ProfileUpdate.as_view()),name="perfil"),
    path('profile/email/',login_required(EmailUpdate.as_view()),name="profile_email"),
]
