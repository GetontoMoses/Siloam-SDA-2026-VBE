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
    path("age-groups/", AgeGroupListCreateView.as_view(), name="age-group-list-create"),
    path("age-groups/<int:pk>/", AgeGroupDetailView.as_view(), name="age-group-detail"),
    # Registrations
    path(
        "registrations/",
        RegistrationListCreateView.as_view(),
        name="registration-list-create",
    ),
    path(
        "registrations/<int:pk>/",
        RegistrationDetailView.as_view(),
        name="registration-detail",
    ),
    # Attendance
    path(
        "attendance/", AttendanceListCreateView.as_view(), name="attendance-list-create"
    ),
    path(
        "attendance/<int:pk>/", AttendanceDetailView.as_view(), name="attendance-detail"
    ),
    # Lessons
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list-create"),
    path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
    # Activities
    path("activities/", ActivityListCreateView.as_view(), name="activity-list-create"),
    path("activities/<int:pk>/", ActivityDetailView.as_view(), name="activity-detail"),
]
