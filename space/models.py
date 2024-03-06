from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

UserRoles = (("buyer", "Buyer"), ("seller", "Seller"))
GenderChoice = (("male", "Male"), ("female", "Female"), ("other", "Other"))


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    role = models.CharField(choices=UserRoles, max_length=50)
    contact_number = models.CharField(max_length=13)
    gender = models.CharField(choices=GenderChoice, max_length=10)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Workspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    workspace_name = models.CharField(max_length=200)
    desk = models.IntegerField()

    def __str__(self):
        return self.workspace_name


class SpaceCategory(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        verbose_name_plural = "Space categories"

    def __str__(self) -> str:
        return self.name


# related_name : reverse relationship
class WorkspaceImage(models.Model):
    workspace_name = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="workspace_images"
    )
    images = models.ImageField(upload_to="images")
    category = models.ForeignKey(
        SpaceCategory, on_delete=models.CASCADE, related_name="category"
    )

    def __str__(self):
        return self.workspace_name.workspace_name

    def get_amount(self):
        return self.category.price

    def get_seller_name(self):
        user = self.workspace_name.user
        return user.first_name + " " + user.last_name
