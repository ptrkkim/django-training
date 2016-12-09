from django.test import TestCase

from src.core_auth.forms import UserCreationForm
from src.core_auth.models import User


class UserCreationFormTests(TestCase):

    def setUp(self):
        self.data = {'email': 'foo@example.com', 'password1': '123abc', 'password2': '123abc'}

    def test_create_user_given_valid_data(self):
        form = UserCreationForm(self.data)
        assert form.is_valid() is True

        user = form.save()
        assert user.id
        assert user.check_password('123abc') is True

    def test_required_fields(self):
        required_fields = ['email', 'password1', 'password2']

        form = UserCreationForm({})
        assert form.is_valid() is False

        assert len(required_fields) == len(form.errors)
        for field in required_fields:
            assert field in form.errors

    def test_passwords_must_match(self):
        self.data['password2'] = 'xpto'

        form = UserCreationForm({})
        assert form.is_valid() is False

        assert 'password2' in form.errors
