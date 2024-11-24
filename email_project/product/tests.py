from django.test import TestCase, Client
from django.core.cache import cache
from .models import ProductDataset

class GetDatasetsByStatusTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.status = 'pending'
        ProductDataset.objects.create(file='uploads/test1.csv', status=self.status)
        ProductDataset.objects.create(file='uploads/test2.csv', status='completed')

    def test_get_datasets_by_status(self):
        cache.clear()
        response = self.client.get(f'/products/datasets/{self.status}/')
        self.assertEqual(response.status_code, 200)
        datasets = response.json().get('datasets')
        self.assertEqual(len(datasets), 1)
        self.assertEqual(datasets[0]['status'], self.status)

        with self.assertNumQueries(0):
            response = self.client.get(f'/products/datasets/{self.status}/')
            self.assertEqual(response.status_code, 200)
