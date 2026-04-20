from rest_framework import serializers
from .models import (
    Guardian,
    Child,
    Attendance,
    Teacher,
    Station
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


class AttendanceSerializer(serializers.ModelSerializer):
    child_name = serializers.CharField(
        source="registration.child.full_name",
        read_only=True,
    )

    class Meta:
        model = Attendance
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"
