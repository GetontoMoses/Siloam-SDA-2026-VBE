from django.db import models

class User(AbstractUser):
    Role_Choices = (
        ("admin", "Admin"),
        ("coordinator", "Coordinator"),
        ("teacher", "Teacher"),
        ("volunteer", "Volunteer"),
        ("registrar", "Registrar"),
    )
