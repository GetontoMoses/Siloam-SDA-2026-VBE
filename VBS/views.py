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
