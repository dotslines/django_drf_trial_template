import datetime
from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F
from django.core.cache import cache


@shared_task(base=Singleton)
def set_price(subscription_id):
    """
    Sets price to the subscription.
    """
    from .models import Subscription

    # fp - (fp * discount)/100
    price_formula = (
        F('service__full_price') -
        F('service__full_price') *
        F('plan__discount_percent') / 100
    )

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update(
                ).filter(
                    id=subscription_id
                ).annotate(
                    annotated_price=price_formula
                ).first()
        subscription.price = subscription.annotated_price
        subscription.save()

    # cache invalidation
    cache.delete('price_cached')


@shared_task(base=Singleton)
def set_comment(subscription_id):
    """
    Set an comment to the subscription.
    """
    from .models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update(
                                          ).get(id=subscription_id)
        subscription.comment = str(datetime.datetime.now())
        subscription.save()
