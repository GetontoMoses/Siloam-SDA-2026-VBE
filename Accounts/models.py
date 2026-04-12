from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("coordinator", "Coordinator"),
        ("teacher", "Teacher"),
        ("volunteer", "Volunteer"),
        ("registrar", "Registrar"),
    )

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="volunteer")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    objects = UserManager()

    def __str__(self):
        return self.full_name or self.email
