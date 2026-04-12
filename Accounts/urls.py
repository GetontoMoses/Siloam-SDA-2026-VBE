from django.urls import path
from .views import UserListCreateView, UserDetailView, EmailLoginView

urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="email-login"),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
