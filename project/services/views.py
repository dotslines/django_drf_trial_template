from django.shortcuts import render
from django.db.models import F, Prefetch, Sum
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Subscription.objects.all(
            ).prefetch_related(
                'plan',
                Prefetch(
                    'account',
                    queryset=Account.objects.all(
                                            ).select_related('user'
                                            ).only('company_name', 'user__email')
                )
            )
    serializer_class = SubscriptionSerializer
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        price_cached = cache.get(settings.PRICE_CACHED_NAME)
        
        if price_cached:
            total = price_cached
        else:
            qs = self.filter_queryset(self.get_queryset())     # to apply filter backends
            total = qs.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHED_NAME, total, 10)
        
        modified_response = {
            'subscriptions': response.data,
            'total': total
        }
        return Response(modified_response)
