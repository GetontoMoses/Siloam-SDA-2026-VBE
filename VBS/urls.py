from django.urls import path
from .views import (
    GuardianListCreateView,
    GuardianDetailView,
    ChildListCreateView,
    ChildDetailView,
    AttendanceListCreateView,
    AttendanceDetailView,
    TeacherListCreateView,
    TeacherDetailView,
    StationListCreateView,
    StationDetailView,
)

urlpatterns = [
    path("guardians/", GuardianListCreateView.as_view(), name="guardian-list"),
    path("guardians/<int:pk>/", GuardianDetailView.as_view(), name="guardian-detail"),
    path("children/", ChildListCreateView.as_view(), name="child-list"),
    path("children/<int:pk>/", ChildDetailView.as_view(), name="child-detail"),
    path("attendance/", AttendanceListCreateView.as_view(), name="attendance-list"),
    path(
        "attendance/<int:pk>/", AttendanceDetailView.as_view(), name="attendance-detail"
    ),
    path("teachers/", TeacherListCreateView.as_view(), name="teacher-list"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teacher-detail"),
    path("stations/", StationListCreateView.as_view(), name="station-list"),
    path("stations/<int:pk>/", StationDetailView.as_view(), name="station-detail"),
]
