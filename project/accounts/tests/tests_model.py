from django.test import TestCase
from ..models import Account


class AccountModelTestCase(TestCase):
    """
    Tests for the Account model.
    For now this tests are as simple as possible.
    """
    def setUp(self) -> None:
        """
        Method called to prepare the test fixture.
        This is called immediately before calling the test method.
        """
        # create_user hashes the password
        Account.objects.create_user(
            username="test_account",
            password="secret",
            email="test_email@email.com",
            company_name="GreenPlanet",
            full_address="City, street, home."
        )

    def tearDown(self) -> None:
        """
        Method called immediately after the test method has been called
        and the result recorded.
        This is called even if the test method raised an exception.
        """
        pass

    def test_account_attributes(self) -> None:
        """Test account attributes created correctly."""
        user = Account.objects.get(username="test_account")
        self.assertEqual(user.email, "test_email@email.com")
        self.assertEqual(user.company_name, "GreenPlanet")
        self.assertEqual(user.full_address, "City, street, home.")
