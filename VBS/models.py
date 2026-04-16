from django.conf import settings
from django.db import models
from django.forms import ValidationError


class Guardian(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    relationship_to_child = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    home_church = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medical_notes = models.TextField(blank=True, null=True)
    special_needs = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="children_photos/", blank=True, null=True)
    is_first_time_attendee = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class VBSProgram(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("active", "Active"),
        ("closed", "Closed"),
    )

    title = models.CharField(max_length=255)
    theme = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    venue = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    def __str__(self):
        return self.title


class AgeGroup(models.Model):
    program = models.ForeignKey(
        VBSProgram, on_delete=models.CASCADE, related_name="age_groups"
    )
    name = models.CharField(max_length=100)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    room_name = models.CharField(max_length=100, blank=True, null=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teaching_groups",
    )
    assistant_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assisting_groups",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.max_age < self.min_age:
            raise ValidationError("Max age cannot be less than min age.")

    def __str__(self):
        return f"{self.name} - {self.program.title}"

class Registration(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("cancelled", "Cancelled"),
    )

    child = models.ForeignKey(
        Child, on_delete=models.CASCADE, related_name="registrations"
    )
    program = models.ForeignKey(
        VBSProgram, on_delete=models.CASCADE, related_name="registrations"
    )
    group = models.ForeignKey(
        AgeGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registrations",
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    pickup_notes = models.TextField(blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    amount_remaining = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["child", "program"],
                name="unique_child_program_registration",
            )
        ]

    def __str__(self):
        return f"{self.child} - {self.program}"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
    )

    registration = models.ForeignKey(
        Registration, on_delete=models.CASCADE, related_name="attendance_records"
    )
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="present")
    check_in_time = models.TimeField(blank=True, null=True)
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
                fields=["registration", "date"],
                name="unique_attendance_per_registration_date",
            )
        ]

    def __str__(self):
        return f"{self.registration.child} - {self.date} - {self.status}"


class Lesson(models.Model):
    program = models.ForeignKey(
        VBSProgram, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=255)
    date = models.DateField()
    bible_text = models.CharField(max_length=255, blank=True, null=True)
    memory_verse = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.date}"


class Activity(models.Model):
    program = models.ForeignKey(
        VBSProgram,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_activities",
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return f"{self.name} - {self.day}"
