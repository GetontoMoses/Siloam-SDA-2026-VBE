from django.urls import path
from .views import (
    GuardianListCreateView,
    GuardianDetailView,
    ChildListCreateView,
    ChildDetailView,
    VBSProgramListCreateView,
    VBSProgramDetailView,
    AgeGroupListCreateView,
    AgeGroupDetailView,
    RegistrationListCreateView,
    RegistrationDetailView,
    AttendanceListCreateView,
    AttendanceDetailView,
    LessonListCreateView,
    LessonDetailView,
    ActivityListCreateView,
    ActivityDetailView,
)
urlpatterns = [
    # Guardians
    path("guardians/", GuardianListCreateView.as_view(), name="guardian-list-create"),
    path("guardians/<int:pk>/", GuardianDetailView.as_view(), name="guardian-detail"),

    # Children
    path("children/", ChildListCreateView.as_view(), name="child-list-create"),
    path("children/<int:pk>/", ChildDetailView.as_view(), name="child-detail"),

    # Programs
    path("programs/", VBSProgramListCreateView.as_view(), name="program-list-create"),
    path("programs/<int:pk>/", VBSProgramDetailView.as_view(), name="program-detail"),

    # Age Groups