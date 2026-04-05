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
