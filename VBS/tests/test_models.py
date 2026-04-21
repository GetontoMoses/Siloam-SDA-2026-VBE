from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time

from VBS.models import Guardian, Child, Attendance, Teacher, Station

User = get_user_model()


class GuardianModelTest(TestCase):
    def test_create_guardian(self):
        guardian = Guardian.objects.create(
            full_name="John Doe", phone_number="0712345678"
        )
        self.assertEqual(str(guardian), "John Doe")


class ChildModelTest(TestCase):
    def setUp(self):
        self.guardian = Guardian.objects.create(
            full_name="Jane Doe", phone_number="0798765432"
        )

    def test_child_full_name(self):
        child = Child.objects.create(
            guardian=self.guardian,
            first_name="Baby",
            last_name="Doe",
            gender="male",
            age_group="5-7",
        )
        self.assertEqual(child.full_name, "Baby Doe")


class AttendanceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester")
        self.guardian = Guardian.objects.create(
            full_name="Parent", phone_number="0700000000"
        )
        self.child = Child.objects.create(
            guardian=self.guardian,
            first_name="Kid",
            last_name="One",
            gender="male",
            age_group="5-7",
        )

    def test_create_attendance(self):
        attendance = Attendance.objects.create(
            child=self.child,
            date=date.today(),
            status="present",
            check_in_time=time(9, 0),
            marked_by=self.user,
        )
        self.assertEqual(attendance.status, "present")


class TeacherModelTest(TestCase):
    def test_create_teacher(self):
        teacher = Teacher.objects.create(full_name="Tr Smith", role="lead_teacher")
        self.assertEqual(teacher.role, "lead_teacher")


class StationModelTest(TestCase):
    def test_create_station(self):
        teacher = Teacher.objects.create(full_name="Tr Smith", role="lead_teacher")
        station = Station.objects.create(name="Station 1", teacher=teacher)
        self.assertEqual(station.name, "Station 1")
