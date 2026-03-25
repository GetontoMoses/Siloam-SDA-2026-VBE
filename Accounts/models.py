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
