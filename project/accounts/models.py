# from django.db import models
# from django.contrib.auth import get_user_model


# USER_MODEL = get_user_model()


# class Account(models.Model):
#     """
#     Account profile for an user.
#     """
#     user = models.OneToOneField(USER_MODEL, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=150, blank=True)
#     full_address = models.CharField(max_length=150, blank=True)

#     def __str__(self) -> str:
#         return f'Client: {self.company_name}'

from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    """
    The project default User model.
    """
    company_name = models.CharField(max_length=150, blank=True)
    full_address = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
        ordering = 'username',

    def __str__(self) -> str:
        return f'Client: {self.company_name}'
