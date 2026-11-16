import json
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User


class PortalTests(TestCase):
    def test_authentication_and_logout(self):
        User.objects.create_user(username='driver', password='test-password-42')
        response = self.client.post('/djangoapp/login', json.dumps({'userName': 'driver', 'password': 'wrong'}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/djangoapp/login', json.dumps({'userName': 'driver', 'password': 'test-password-42'}), content_type='application/json')
        self.assertEqual(response.json()['status'], 'Authenticated')
        self.client.get('/djangoapp/logout')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_registration_rejects_duplicate(self):
        data = {'userName': 'newdriver', 'password': 'test-password-42', 'firstName': 'Test', 'lastName': 'Driver', 'email': 'driver@example.com'}
        self.assertEqual(self.client.post('/djangoapp/register', json.dumps(data), content_type='application/json').status_code, 201)
        self.assertEqual(self.client.post('/djangoapp/register', json.dumps(data), content_type='application/json').status_code, 409)

    def test_review_requires_login(self):
        self.assertEqual(self.client.post('/djangoapp/add_review', '{}', content_type='application/json').status_code, 401)

    @patch('djangoapp.views.get_request', return_value=[{'id': 1, 'state': 'Kansas'}])
    def test_state_filter_proxy(self, get_request):
        response = self.client.get('/djangoapp/get_dealers/Kansas')
        self.assertEqual(response.json()['dealers'][0]['state'], 'Kansas')
        get_request.assert_called_once_with('fetchDealers/Kansas')
