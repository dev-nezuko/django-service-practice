from django.test import TestCase
from rest_framework.test import APIClient

class ExistingInventoryReadTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_empty_inventory_list(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_missing_inventory_and_taxonomy_are_404(self):
        for path in ['/inventory/999/', '/inventory/tags/999/', '/inventory/types/999/', '/inventory/languages/999/']:
            for method in ['get', 'patch', 'delete']:
                with self.subTest(path=path, method=method):
                    response = getattr(self.client, method)(path, {}, format='json')
                    self.assertEqual(response.status_code, 404)

    def test_existing_empty_order_routes(self):
        for path in ['/orders/', '/orders/tags/']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), [])
