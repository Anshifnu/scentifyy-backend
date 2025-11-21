
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)
    isBlock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    # ⚡ Use email for login
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'      # makes email the unique identifier
    REQUIRED_FIELDS = ['username']  # username is still required for Django admin

    def __str__(self):
        return f"{self.email} ({self.role})"



