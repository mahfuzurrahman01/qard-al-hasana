from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from organization.managers import UserManager
from peoples.models import Staff


class Division(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Thana(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    code = models.IntegerField(unique=True, db_index=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=150)
    branch = models.ForeignKey("organization.Branch", on_delete=models.CASCADE)
    owner = models.OneToOneField(Staff, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "branch")

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=45)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.username


class OrgMember(models.Model):
    member_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=14)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.member_name


class Branch(models.Model):
    name = models.CharField(max_length=255)
    code = models.IntegerField(db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    bank_account = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [["organization", "code"], ["organization", "name"]]

    def __str__(self):
        return self.name


class BranchMember(models.Model):
    name = models.CharField(max_length=150)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
