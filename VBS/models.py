from django.conf import settings
from django.db import models
from django.forms import ValidationError


class Guardian(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    relationship_to_child = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name


class Child(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    guardian = models.ForeignKey(
        Guardian, on_delete=models.CASCADE, related_name="children"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age_group = models.CharField(max_length=255, blank=False, null=False, default="6-9")
    allergies = models.TextField(blank=True, null=True)
    medical_notes = models.TextField(blank=True, null=True)
    special_needs = models.TextField(blank=True, null=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Attendance(models.Model):
    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
    )
    child = models.ForeignKey(
        Child, on_delete=models.CASCADE, related_name="attendance_records"
    )
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="present")
    check_in_time = models.TimeField(blank=False, null=False)
    check_out_time = models.TimeField(blank=True, null=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marked_attendance_records",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["child", "date"],
                name="unique_attendance_per_child_date",
            )
        ]

    def __str__(self):
        return f"{self.child} - {self.date} - {self.status}"


class Teacher(models.Model):
    ROLE_CHOICES = [
        ("lead_teacher", "Lead Teacher"),
        ("assistant_teacher", "Assistant Teacher"),
        ("support_staff", "Support Staff"),
        ("volunteer", "Volunteer"),
    ]
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="volunteer")
    is_on_duty = models.BooleanField(default=False)
    duty_date = models.DateField(blank=True, null=True)


class Station(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_stations",
    )
    venue = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return f"{self.name} - {self.day}"
