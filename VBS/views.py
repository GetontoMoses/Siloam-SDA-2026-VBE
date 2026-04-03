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
