from datetime import date, time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from VBS.models import Guardian, Child, Attendance, Teacher, Station

User = get_user_model()


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass1234"
        )

        self.guardian = Guardian.objects.create(
            full_name="Jane Doe",
            phone_number="0712345678",
            email="jane@example.com",
            relationship_to_child="Mother",
            address="Nairobi",
            emergency_contact_name="John Doe",
            emergency_contact_phone="0799999999",
        )

        self.child = Child.objects.create(
            guardian=self.guardian,
            first_name="Tim",
            last_name="Doe",
            gender="male",
            age_group="6-8",
            allergies="Peanuts",
            medical_notes="None",
            special_needs="None",
        )

        self.teacher = Teacher.objects.create(
            full_name="Mr. Smith",
            email="smith@example.com",
            phone_number="0700000000",
            role="lead_teacher",
            is_on_duty=True,
            duty_date=date.today(),
        )

        self.station = Station.objects.create(
            name="Bible Study",
            description="Morning station",
            teacher=self.teacher,
            venue="Hall A",
        )

        self.attendance = Attendance.objects.create(
            child=self.child,
            date=date.today(),
            status="present",
            check_in_time=time(8, 0),
            check_out_time=time(12, 0),
            marked_by=self.user,
        )

    def authenticate(self):
        self.client.force_authenticate(user=self.user)


class GuardianViewTest(BaseAPITestCase):
    def test_list_guardians(self):
        url = reverse("guardian-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_guardian(self):
        url = reverse("guardian-detail", args=[self.guardian.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], "Jane Doe")

    def test_create_guardian_unauthenticated(self):
        url = reverse("guardian-list")
        data = {
            "full_name": "New Guardian",
            "phone_number": "0701111111",
            "email": "newguardian@example.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_guardian_authenticated(self):
        self.authenticate()
        url = reverse("guardian-list")
        data = {
            "full_name": "New Guardian",
            "phone_number": "0701111111",
            "email": "newguardian@example.com",
            "relationship_to_child": "Aunt",
            "address": "Mombasa",
            "emergency_contact_name": "Emergency Person",
            "emergency_contact_phone": "0711111111",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_guardian_authenticated(self):
        self.authenticate()
        url = reverse("guardian-detail", args=[self.guardian.id])
        data = {
            "full_name": "Jane Updated",
            "phone_number": "0712345678",
            "email": "janeupdated@example.com",
            "relationship_to_child": "Mother",
            "address": "Updated Address",
            "emergency_contact_name": "John Doe",
            "emergency_contact_phone": "0799999999",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.guardian.refresh_from_db()
        self.assertEqual(self.guardian.full_name, "Jane Updated")

    def test_delete_guardian_authenticated(self):
        self.authenticate()
        url = reverse("guardian-detail", args=[self.guardian.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Guardian.objects.filter(id=self.guardian.id).exists())


class ChildViewTest(BaseAPITestCase):
    def test_list_children(self):
        url = reverse("child-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_child(self):
        url = reverse("child-detail", args=[self.child.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Tim")

    def test_create_child_unauthenticated(self):
        url = reverse("child-list")
        data = {
            "guardian": self.guardian.id,
            "first_name": "Anna",
            "last_name": "Doe",
            "gender": "female",
            "age_group": "9-12",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_child_authenticated(self):
        self.authenticate()
        url = reverse("child-list")
        data = {
            "guardian": self.guardian.id,
            "first_name": "Anna",
            "last_name": "Doe",
            "gender": "female",
            "age_group": "9-12",
            "allergies": "Dust",
            "medical_notes": "Asthma",
            "special_needs": "None",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_child_authenticated(self):
        self.authenticate()
        url = reverse("child-detail", args=[self.child.id])
        data = {
            "guardian": self.guardian.id,
            "first_name": "Timothy",
            "last_name": "Doe",
            "gender": "male",
            "age_group": "6-8",
            "allergies": "Peanuts",
            "medical_notes": "Updated notes",
            "special_needs": "None",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.child.refresh_from_db()
        self.assertEqual(self.child.first_name, "Timothy")

    def test_delete_child_authenticated(self):
        self.authenticate()
        url = reverse("child-detail", args=[self.child.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Child.objects.filter(id=self.child.id).exists())


class AttendanceViewTest(BaseAPITestCase):
    def test_list_attendance(self):
        url = reverse("attendance-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_attendance(self):
        url = reverse("attendance-detail", args=[self.attendance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_attendance_unauthenticated(self):
        url = reverse("attendance-list")
        data = {
            "child": self.child.id,
            "date": str(date.today()),
            "status": "present",
            "check_in_time": "08:30:00",
            "check_out_time": "12:30:00",
            "marked_by": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_attendance_authenticated(self):
        self.authenticate()

        another_child = Child.objects.create(
            guardian=self.guardian,
            first_name="Sam",
            last_name="Doe",
            gender="male",
            age_group="9-12",
        )

        url = reverse("attendance-list")
        data = {
            "child": another_child.id,
            "date": "2026-04-20",
            "status": "present",
            "check_in_time": "08:30:00",
            "check_out_time": "12:30:00",
            "marked_by": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_attendance_authenticated(self):
        self.authenticate()
        url = reverse("attendance-detail", args=[self.attendance.id])
        data = {
            "child": self.child.id,
            "date": str(self.attendance.date),
            "status": "absent",
            "check_in_time": "08:00:00",
            "check_out_time": "12:00:00",
            "marked_by": self.user.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.status, "absent")

    def test_delete_attendance_authenticated(self):
        self.authenticate()
        url = reverse("attendance-detail", args=[self.attendance.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Attendance.objects.filter(id=self.attendance.id).exists())


class TeacherViewTest(BaseAPITestCase):
    def test_list_teachers(self):
        url = reverse("teacher-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_teacher(self):
        url = reverse("teacher-detail", args=[self.teacher.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], "Mr. Smith")

    def test_create_teacher_unauthenticated(self):
        url = reverse("teacher-list")
        data = {
            "full_name": "Mrs. Faith",
            "email": "faith@example.com",
            "phone_number": "0711111222",
            "role": "assistant_teacher",
            "is_on_duty": True,
            "duty_date": str(date.today()),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_teacher_authenticated(self):
        self.authenticate()
        url = reverse("teacher-list")
        data = {
            "full_name": "Mrs. Faith",
            "email": "faith@example.com",
            "phone_number": "0711111222",
            "role": "assistant_teacher",
            "is_on_duty": True,
            "duty_date": str(date.today()),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_teacher_authenticated(self):
        self.authenticate()
        url = reverse("teacher-detail", args=[self.teacher.id])
        data = {
            "full_name": "Mr. Smith Updated",
            "email": "smithupdated@example.com",
            "phone_number": "0700000000",
            "role": "lead_teacher",
            "is_on_duty": False,
            "duty_date": str(date.today()),
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.full_name, "Mr. Smith Updated")

    def test_delete_teacher_authenticated(self):
        self.authenticate()
        url = reverse("teacher-detail", args=[self.teacher.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Teacher.objects.filter(id=self.teacher.id).exists())


class StationViewTest(BaseAPITestCase):
    def test_list_stations(self):
        url = reverse("station-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_station(self):
        url = reverse("station-detail", args=[self.station.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Bible Study")

    def test_create_station_unauthenticated(self):
        url = reverse("station-list")
        data = {
            "name": "Crafts",
            "description": "Creative station",
            "teacher": self.teacher.id,
            "venue": "Room B",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_station_authenticated(self):
        self.authenticate()
        url = reverse("station-list")
        data = {
            "name": "Crafts",
            "description": "Creative station",
            "teacher": self.teacher.id,
            "venue": "Room B",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_station_authenticated(self):
        self.authenticate()
        url = reverse("station-detail", args=[self.station.id])
        data = {
            "name": "Bible Study Updated",
            "description": "Updated station",
            "teacher": self.teacher.id,
            "venue": "Hall B",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.station.refresh_from_db()
        self.assertEqual(self.station.name, "Bible Study Updated")

    def test_delete_station_authenticated(self):
        self.authenticate()
        url = reverse("station-detail", args=[self.station.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Station.objects.filter(id=self.station.id).exists())
