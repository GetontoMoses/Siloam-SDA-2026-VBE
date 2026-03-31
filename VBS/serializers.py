from rest_framework import serializers
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


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = "__all__"


class ChildSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Child
        fields = "__all__"
