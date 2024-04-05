import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import gettext_lazy as _

import uuid
import time
from datetime import datetime

from user.utils import COUNTRIES
from django.contrib.auth.models import AbstractUser


# Create your models here.
def generate_unique_key():
    return str(uuid.uuid4())


def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)


User.add_to_class("Address", models.JSONField(default={}, blank=True, null=True))


# class User(AbstractBaseUser, PermissionsMixin):
#     id = models.UUIDField(
#         default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True
#     )
#     email = models.EmailField(_("email address"), blank=True, unique=True)
#     profile_pic = models.CharField(
#         max_length=1000, null=True, blank=True
#     )
#     activation_key = models.CharField(max_length=150, null=True, blank=True)
#     key_expires = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]
#
#     objects = UserManager()
#
#     class Meta:
#         verbose_name = "User"
#         verbose_name_plural = "Users"
#         db_table = "users"
#         ordering = ("-is_active",)
#
#     def __str__(self):
#         return self.email


class Address(models.Model):
    address_line = models.CharField(
        _("Address"), max_length=255, blank=True, default=""
    )
    street = models.CharField(_("Street"), max_length=55, blank=True, default="")
    city = models.CharField(_("City"), max_length=255, blank=True, default="")
    state = models.CharField(_("State"), max_length=255, blank=True, default="")
    postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, default=""
    )
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, default="")
    created_at = models.DateTimeField(default=datetime.now())

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        db_table = "address"
        ordering = ("-created_at",)

    def __str__(self):
        return self.city if self.city else ""

    def get_complete_address(self):
        address = ""
        if self.address_line:
            address += self.address_line
        if self.street:
            if address:
                address += ", " + self.street
            else:
                address += self.street
        if self.city:
            if address:
                address += ", " + self.city
            else:
                address += self.city
        if self.state:
            if address:
                address += ", " + self.state
            else:
                address += self.state
        if self.postcode:
            if address:
                address += ", " + self.postcode
            else:
                address += self.postcode
        if self.country:
            if address:
                address += ", " + self.get_country_display()
            else:
                address += self.get_country_display()
        return address
