from rest_framework import serializers 

from .models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Plan
        fields = ('id', 'plan_type', 'discount_percent')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    account_name = serializers.CharField(source='account.company_name')
    email = serializers.CharField(source='account.email')
    price = serializers.SerializerMethodField()   # will look for the 'get_price' method
    
    def get_price(self, instance):
        return instance.price
        # this was passed into the APIView query
        # full_price = instance.service.full_price
        # return (
        #     full_price - 
        #     (full_price * instance.plan.discount_percent / 100)
        # )
    
    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'account_name', 'email', 'plan', 'price')
