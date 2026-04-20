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
    # Guardians
    path("guardians/", GuardianListCreateView.as_view(), name="guardian-list-create"),
    path("guardians/<int:pk>/", GuardianDetailView.as_view(), name="guardian-detail"),
    # Children
    path("children/", ChildListCreateView.as_view(), name="child-list-create"),
    path("children/<int:pk>/", ChildDetailView.as_view(), name="child-detail"),
    # Attendance
    path(
        "attendance/", AttendanceListCreateView.as_view(), name="attendance-list-create"
    ),
    path(
        "attendance/<int:pk>/", AttendanceDetailView.as_view(), name="attendance-detail"
    ),
    # Teachers
    path("teachers/", TeacherListCreateView.as_view(), name="teacher-list-create"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teacher-detail"),
    # Stations
    path("stations/", StationListCreateView.as_view(), name="station-list-create"),
    path("stations/<int:pk>/", StationDetailView.as_view(), name="station-detail"),
]
