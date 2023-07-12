from django.contrib import admin

from .models import Plan, Service, Subscription


admin.site.register(Plan)
admin.site.register(Service)
admin.site.register(Subscription)
