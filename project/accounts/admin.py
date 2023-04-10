# from django.contrib import admin

# from .models import Account


# admin.site.register(Account)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('username', 'email')
    list_display_links = ('username', 'email')
