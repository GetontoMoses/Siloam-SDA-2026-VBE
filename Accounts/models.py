from django.db import models

class User(AbstractUser):
    Role_Choices = (
        ("admin", "Admin"),
        ("coordinator", "Coordinator"),
        ("teacher", "Teacher"),
        ("volunteer", "Volunteer"),
        ("registrar", "Registrar"),
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role_Choices, default="volunteer")

    def __str__(self):
        return self.full_name or self.username

class Guardian(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    relationship_to_child = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    home_church = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name

class Child(model.Model):
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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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

    def __str__(self):
        return self.title

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
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    pickup_notes = models.TextField(blank=True, null=True)
    

    class Meta:
        unique_together = ("child", "program")

    def __str__(self):
        return f"{self.child} - {self.program}"

class AgeGroup(models.Model):
    program = models.ForeignKey(
        VBSProgram, on_delete=models.CASCADE, related_name="age_groups"
    )
    name = models.CharField(max_length=100)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    room_name = models.CharField(max_length=100, blank=True, null=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teaching_groups",
    )

    def __str__(self):
        return f"{self.name} - {self.program.title}"

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
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        unique_together = ("registration", "date")

    def __str__(self):
        return f"{self.registration.child} - {self.date} - {self.status}"

class Lesson(models.Model):