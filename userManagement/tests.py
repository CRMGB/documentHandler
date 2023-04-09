import json
from django.test import TestCase
from django.contrib.auth.models import User


class UserTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        """ User already saved in the db """
        response = self.client.post('/login', self.credentials, follow=True)
        # should be logged in now
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_register_and_login(self):
        """Create user using the register endpoint and then login"""
        new_user = {
            'username': 'registereduser',
            'email': 'fake@email.com',
            'password1': 'secret_2',
            'password2': 'secret_2',
        }
        response = self.client.post('', new_user, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(
            response, '/csv_upload',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        response_login = self.client.post('/login', new_user, follow=True)
        # should be logged in now
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_login.context['user'].is_authenticated)
