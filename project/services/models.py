from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete

from accounts.models import Account
from .tasks import set_price
from .receivers import invalidate_cached_price


class Service(models.Model):
    name = models.CharField(max_length=200)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price
    
    def __str__(self):
        return f'Service: {self.name}'
    
    def save(self, *args, **kwargs):
        if self.__full_price != self.full_price:
            subscriptions = self.subscriptions.all()
            for subscription in subscriptions:
                set_price.delay(subscription.id)
        
        return super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )
    
    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10, default=PLAN_TYPES[0][0])
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent
    
    def __str__(self):
        return f'Plan: {self.plan_type}'
    
    def save(self, *args, **kwargs):
        if self.__discount_percent != self.discount_percent:
            subscriptions = self.subscriptions.all()
            for subscription in subscriptions:
                set_price.delay(subscription.id)
        
        return super().save(*args, **kwargs)


class Subscription(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f'Subscription: {self.id}'
    
    def save(self, *args, **kwargs):
        creating = not bool(self.id)
        result = super().save(*args, **kwargs)
        if creating:
            set_price.delay(self.id)
        return result
        

post_delete.connect(invalidate_cached_price)