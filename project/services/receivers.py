from django.core.cache import cache


def invalidate_cached_price(**kwargs):
    cache.delete('price_cached')
