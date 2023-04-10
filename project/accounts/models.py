# from django.db import models
# from django.contrib.auth import get_user_model


# USER_MODEL = get_user_model()


# class Account(models.Model):
    
#     user = models.OneToOneField(USER_MODEL, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=150, blank=True)
#     full_address = models.CharField(max_length=150, blank=True)
    
#     def __str__(self):
#         return f'Client: {self.company_name}'

from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    company_name = models.CharField(max_length=150, blank=True)
    full_address = models.CharField(max_length=150, blank=True)
    
    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
        ordering = 'username',
    
    def __str__(self):
        return f'Client: {self.company_name}'
