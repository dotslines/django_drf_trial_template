from django.test import TestCase
from accounts.models import Account

from ..models import Plan, Service, Subscription


class ModelsTestCase(TestCase):
    """
    Tests for the models.
    For now this tests are as simple as possible.
    """
    def setUp(self) -> None:
        """
        Method called to prepare the test fixture.
        This is called immediately before calling the test method.
        """
        Account.objects.create_user(
            username="test_account",
            password="secret",
            email="test_email@email.com",
            company_name="GreenPlanet",
            full_address="City, street, home."
        )
        Plan.objects.create()
        Service.objects.create(
            name="test_service",
            full_price=1000,
        )

    def tearDown(self) -> None:
        """
        Method called immediately after the test method has been called
        and the result recorded.
        This is called even if the test method raised an exception.
        """
        pass

    def test_service_created_properly(self) -> None:
        """Test service attributes created correctly."""
        service = Service.objects.get(name="test_service")
        self.assertEqual(service.full_price, 1000)

    def test_plan_created_properly(self) -> None:
        """Test plan attributes created correctly."""
        plan = Plan.objects.first()
        self.assertEqual(plan.plan_type, Plan.PLAN_TYPES[0][0])
        self.assertEqual(plan.discount_percent, 0)

    def test_subscription_created_properly(self) -> None:
        """Test subscription attributes created correctly."""
        user = Account.objects.get(username="test_account")
        service = Service.objects.get(name="test_service")
        plan = Plan.objects.first()
        subscription = Subscription.objects.create(
            account=user,
            plan=plan,
            service=service,
            comment="test comment!"
        )
        price = service.full_price -\
            service.full_price *\
            plan.discount_percent / 100
        self.assertEqual(subscription.user, user.id)
        self.assertEqual(subscription.price, price)
        self.assertEqual(subscription.plan, plan.id)
        self.assertEqual(subscription.service, service.id)
        self.assertEqual(subscription.comment, "test comment!")
