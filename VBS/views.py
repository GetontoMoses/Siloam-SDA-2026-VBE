from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import Guardian, Child, Attendance, Teacher, Station
from .serializers import (
    GuardianSerializer,
    ChildSerializer,
    AttendanceSerializer,
    TeacherSerializer,
    StationSerializer,
)


# Guardian Views
class GuardianListCreateView(generics.ListCreateAPIView):
    queryset = Guardian.objects.all().order_by("-id")
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GuardianDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Child Views
class ChildListCreateView(generics.ListCreateAPIView):
    queryset = Child.objects.select_related("guardian").all().order_by("-id")
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ChildDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Child.objects.select_related("guardian").all()
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Attendance Views
class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = (
        Attendance.objects.select_related(
            "child",
            "marked_by",
        )
        .all()
        .order_by("-date")
    )
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.select_related(
        "child",
        "marked_by",
    ).all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Teacher Views
class TeacherListCreateView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all().order_by("-id")
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Station Views
class StationListCreateView(generics.ListCreateAPIView):
    queryset = Station.objects.select_related(
        "teacher",
    ).all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Station.objects.select_related(
        "teacher",
    ).all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
