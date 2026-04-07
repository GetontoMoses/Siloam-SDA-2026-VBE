from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import (
    Guardian,
    Child,
    VBSProgram,
    AgeGroup,
    Registration,
    Attendance,
    Lesson,
    Activity,
)
from .serializers import (
    GuardianSerializer,
    ChildSerializer,
    VBSProgramSerializer,
    AgeGroupSerializer,
    RegistrationSerializer,
    AttendanceSerializer,
    LessonSerializer,
    ActivitySerializer,
)
# Guardian Views
class GuardianListCreateView(generics.ListCreateAPIView):
    queryset = Guardian.objects.all().order_by("-created_at")
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GuardianDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Child Views
class ChildListCreateView(generics.ListCreateAPIView):
    queryset = Child.objects.select_related("guardian").all().order_by("-created_at")
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ChildDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Child.objects.select_related("guardian").all()
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# VBS Program Views
class VBSProgramListCreateView(generics.ListCreateAPIView):
    queryset = VBSProgram.objects.all().order_by("-created_at")
    serializer_class = VBSProgramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VBSProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VBSProgram.objects.all()
    serializer_class = VBSProgramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Age Group Views
class AgeGroupListCreateView(generics.ListCreateAPIView):
    queryset = (
        AgeGroup.objects.select_related("program", "teacher", "assistant_teacher")
        .all()
        .order_by("-created_at")
    )
    serializer_class = AgeGroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AgeGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AgeGroup.objects.select_related(
        "program", "teacher", "assistant_teacher"
    ).all()
    serializer_class = AgeGroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Registration Views
class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = (
        Registration.objects.select_related("child", "program", "group")
        .all()
        .order_by("-registration_date")
    )
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registration.objects.select_related("child", "program", "group").all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Attendance Views
class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = (
        Attendance.objects.select_related(
            "registration",
            "registration__child",
            "marked_by",
        )
        .all()
        .order_by("-date")
    )
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.select_related(
        "registration",
        "registration__child",
        "marked_by",
    ).all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Lesson Views
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.select_related("program").all().order_by("-date")
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.select_related("program").all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
# Activity Views
class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = (
        Activity.objects.select_related(
            "program",
            "leader",
        )
        .all()
        .order_by("-day", "start_time")
    )
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.select_related(
        "program",
        "leader",
    ).all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
