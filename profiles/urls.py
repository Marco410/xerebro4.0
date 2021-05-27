from django.urls import path
from .views import ProfileListView, ProfileDetailView
from django.contrib.auth.decorators import login_required

profiles_patterns = ([
    path('', ProfileListView.as_view(), name='list'),
    path('<username>/', login_required(ProfileDetailView.as_view()), name='detail'),
], "profiles")
